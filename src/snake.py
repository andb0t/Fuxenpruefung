import math
import random
import sys
import threading
import time
from collections import deque

import tkinter as tk
from PIL import Image
from PIL import ImageTk

import files
import gui_utils
import i18n
import maths
import web_client
try:
    import sound_win as sound
except ImportError:
    import sound_linux as sound


FULL_WIDTH = 800
FULL_HEIGHT = 500
BOX_X_MIN = 0
BOX_X_MAX = 400
BOX_Y_MIN = 50
BOX_Y_MAX = 450
MAX_QUEUE_LEN = 2000
TAIL_STEP_DISTANCE = 6
MAJOR_SIZE = 80
FOX_SIZE = 40
BEER_SIZE = 40
STAR_SIZE = 40
BUCKET_SIZE = 35

MAX_POSITION_LOOPS = 10000
MOVEMENT_STEP_SIZE = 5
MAX_BEER = 11
BEER_RESPAWN_CHANCE = 0.7
N_FREE_FOXES = 3
N_BEERS = 4

START_SPEED = 1 / 50
MAX_SPEED = 4 / 50
N_SPEED_STEPS = 10

START_ROTATION_SPEED = 0.05
MAX_ROTATION_SPEED = 0.10
N_ROTATION_SPEED_STEPS = 10

START_TUMBLE_ANGLE = 5
MAX_TUMBLE_ANGLE = 45
N_TUMBLE_STEPS = 10

N_HIGHSCORES = 20


class SimpleTable(tk.Frame):
    def __init__(self, parent, rows, columns):
        tk.Frame.__init__(self, parent)
        self._widgets = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                relief = 'solid'
                if row > 0:
                    relief = 'groove'
                label = tk.Label(self, borderwidth=1, relief=relief)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)

    def headers(self, headers):
        for col, header in enumerate(headers):
            self.set(0, col, header.capitalize())

    def data(self, scores, keys):
        for row, score in enumerate(scores):
            for col, val in enumerate(score.keys()):
                try:
                    self.set(row + 1, col, score[keys[col]])
                except IndexError:
                    break


class SnakeWindow:

    boxWidth = BOX_X_MAX - BOX_X_MIN
    boxHeight = BOX_Y_MAX - BOX_Y_MIN
    infoBoxWidth = FULL_WIDTH - boxWidth
    infoBoxXMax = FULL_WIDTH
    infoBoxXMin = BOX_X_MAX

    def __init__(self, master):
        gui_utils.center_window(master)

        master.geometry('%sx%s+%s+%s' % (FULL_WIDTH, FULL_HEIGHT, 100, 100))
        master.resizable(0, 0)

        itemRegister = []

        def reset(self):
            self._xPath = deque([], MAX_QUEUE_LEN)
            self._yPath = deque([], MAX_QUEUE_LEN)
            self._xVel = 0
            self._yVel = 0
            self._xVelTumble = 0
            self._yVelTumble = 0
            self._direction = None
            self._score = 0
            self._nFoxes = 0
            self._nBeers = 0
            self._speed = START_SPEED
            self._job = {}
            self._rotationSpeed = 0
            self._currentRotation = 0
            self._tumbleAngle = START_TUMBLE_ANGLE
            self._foxlastXvec = []
            self._foxlastYvec = []
            for idx in range(N_FREE_FOXES):
                self._foxlastXvec.append(random.random())
                self._foxlastYvec.append(random.random())

        def delete_widget(name):
            canv.delete(name)
            try:
                itemRegister.remove(name)
            except ValueError:
                pass

        def _draw_new_fox(newX=None, newY=None, name='fox', size=1):
            if not newX and not newY:
                newX, newY = get_new_random_pos(FOX_SIZE, FOX_SIZE)
                if not newX and not newY:
                    print('Warning: no new free fox position found!')
                    _end_game()
            delete_widget(name)
            thisFoxImgObj = foxImgObj.resize((int(FOX_SIZE * size), int(FOX_SIZE * size)), Image.ANTIALIAS)
            canv.foxImg[name] = ImageTk.PhotoImage(thisFoxImgObj)
            canv.create_image(newX, newY, image=canv.foxImg[name], tags=(name))
            if name not in itemRegister:
                itemRegister.append(name)

        def _draw_new_beer(newX=None, newY=None, name='beer', size=1):
            if not newX and not newY:
                newX, newY = get_new_random_pos(BEER_SIZE, BEER_SIZE)
                if not newX and not newY:
                    print('Warning: no new free beer position found!')
                    _end_game()
            delete_widget(name)
            thisBeerImgObj = beerImgObj.resize((int(BEER_SIZE * size), int(BEER_SIZE * size)), Image.ANTIALIAS)
            canv.beerImg[name] = ImageTk.PhotoImage(thisBeerImgObj)
            canv.create_image(newX, newY, image=canv.beerImg[name], tags=(name))
            if name not in itemRegister:
                itemRegister.append(name)

        def _draw_new_bucket(newX=None, newY=None, name='bucket', size=1):
            if not newX and not newY:
                newX, newY = get_new_random_pos(BUCKET_SIZE, BUCKET_SIZE)
                if not newX and not newY:
                    print('Warning: no new free bucket position found!')
                    _end_game()
            delete_widget(name)
            thisBucketImgObj = bucketImgObj.resize((int(BUCKET_SIZE * size), int(BEER_SIZE * size)), Image.ANTIALIAS)
            canv.bucketImg[name] = ImageTk.PhotoImage(thisBucketImgObj)
            canv.create_image(newX, newY, image=canv.bucketImg[name], tags=(name))
            if name not in itemRegister:
                itemRegister.append(name)

        def _draw_new_star(newX=None, newY=None, name='star', size=1):
            if not newX and not newY:
                newX, newY = get_new_random_pos(STAR_SIZE, STAR_SIZE)
                if not newX and not newY:
                    print('Warning: no new free star position found!')
                    _end_game()
            delete_widget(name)
            thisStarImgObj = starImgObj.resize((int(FOX_SIZE * size), int(FOX_SIZE * size)), Image.ANTIALIAS)
            canv.starImg[name] = ImageTk.PhotoImage(thisStarImgObj)
            canv.create_image(newX, newY, image=canv.starImg[name], tags=(name))
            if name not in itemRegister:
                itemRegister.append(name)

        canv = tk.Canvas(master, highlightthickness=0)
        canv.pack(fill='both', expand=True)

        majorImgObj = Image.open(files.majorImgPath)
        majorImgObj = majorImgObj.resize((MAJOR_SIZE, MAJOR_SIZE), Image.ANTIALIAS)
        canv.majorImg = ImageTk.PhotoImage(majorImgObj)

        foxImgObj = Image.open(files.foxIco)
        foxImgObj = foxImgObj.resize((FOX_SIZE, FOX_SIZE), Image.ANTIALIAS)

        beerImgObj = Image.open(files.beerImgPath)
        beerImgObj = beerImgObj.resize((BEER_SIZE, BEER_SIZE), Image.ANTIALIAS)

        starImgObj = Image.open(files.starImgPath)
        starImgObj = starImgObj.resize((STAR_SIZE, STAR_SIZE), Image.ANTIALIAS)

        bucketImgObj = Image.open(files.bucketImgPath)
        bucketImgObj = bucketImgObj.resize((BUCKET_SIZE, BUCKET_SIZE), Image.ANTIALIAS)

        floorImgObj = Image.open(files.floorImgPath)
        floorImgObj = floorImgObj.resize((BOX_X_MAX - BOX_X_MIN, BOX_Y_MAX - BOX_Y_MIN), Image.ANTIALIAS)
        canv.floorImg = ImageTk.PhotoImage(floorImgObj)

        canv.foxImg = {}
        canv.beerImg = {}
        canv.starImg = {}
        canv.bucketImg = {}

        canv.create_image((BOX_X_MAX + BOX_X_MIN) / 2, (BOX_Y_MAX + BOX_Y_MIN) / 2, image=canv.floorImg, tags=('floor'))

        canv.create_line(0, BOX_Y_MIN, FULL_WIDTH, BOX_Y_MIN, fill='black', tags=('top'), width=10)
        canv.create_line(BOX_X_MIN, BOX_Y_MIN, BOX_X_MIN, BOX_Y_MAX, fill='black', tags=('left'), width=10)
        canv.create_line(BOX_X_MAX - 1, BOX_Y_MIN, BOX_X_MAX - 1, BOX_Y_MAX, fill='black', tags=('middle'), width=10)
        canv.create_line(FULL_WIDTH, BOX_Y_MIN, FULL_WIDTH, BOX_Y_MAX, fill='black', tags=('right'), width=10)
        canv.create_line(0, BOX_Y_MAX - 2, FULL_WIDTH, BOX_Y_MAX - 2, fill='black', tags=('bottom'), width=10)

        canv.create_text(FULL_WIDTH / 2, BOX_Y_MIN * 0.4, text=i18n.snakeWelcome[i18n.lang()],
                         tags=('welcomeText'), font='b', fill='orange')
        canv.create_text(BOX_X_MAX / 2, BOX_Y_MAX * 2 / 8, text=i18n.snakeInstruction[i18n.lang()][0],
                         tags=('instructionText'))
        canv.create_text(BOX_X_MIN + self.boxWidth / 2, BOX_Y_MAX * 6 / 8, text=i18n.snakeInstruction[i18n.lang()][1],
                         tags=('instructionText2'))

        _draw_new_star(BOX_X_MIN + self.boxWidth * 0.30, BOX_Y_MAX * 0.9, "instrStar", 0.5)
        canv.create_text(BOX_X_MIN + self.boxWidth * 0.40, BOX_Y_MAX * 0.9, text='=', tags=('instructionEquals'))
        _draw_new_beer(BOX_X_MIN + self.boxWidth * 0.50, BOX_Y_MAX * 0.9, "instrBeer", 0.5)
        canv.create_text(BOX_X_MIN + self.boxWidth * 0.60, BOX_Y_MAX * 0.9, text='X', tags=('instructionTimes'))
        _draw_new_fox(BOX_X_MIN + self.boxWidth * 0.70, BOX_Y_MAX * 0.9, "instrFox", 0.5)

        canv.create_image(BOX_X_MIN + self.boxWidth * 0.5, BOX_Y_MIN + (BOX_Y_MAX - BOX_Y_MIN) / 2, image=canv.majorImg,
                          tags=('major'))
        itemRegister.append('major')

        def move_fox_tail():
            for idx in range(self._nFoxes):
                thisFoxTag = 'tail' + str(idx)
                try:
                    canv.coords(thisFoxTag,
                                self._xPath[(idx + 1) * TAIL_STEP_DISTANCE],
                                self._yPath[(idx + 1) * TAIL_STEP_DISTANCE])
                except IndexError:
                    pass

        def move_free_fox():
            for idx in range(N_FREE_FOXES):
                name = 'fox' + str(idx)
                x, y = canv.coords(name)
                MAX_ALLOWED_ANGLE = 60
                while True:
                    yShift = (1 - 2 * random.random()) * MOVEMENT_STEP_SIZE
                    xShift = (1 - 2 * random.random()) * MOVEMENT_STEP_SIZE
                    angle = maths.get_angle(xShift, yShift, self._foxlastXvec[idx], self._foxlastYvec[idx])
                    if abs(angle) < MAX_ALLOWED_ANGLE:
                        break
                x, y = x + xShift, y + yShift
                if not check_clipping(x, y, xSize=FOX_SIZE, ySize=FOX_SIZE, exclude=name):
                    self._foxlastXvec[idx] = xShift
                    self._foxlastYvec[idx] = yShift
                    canv.move(name, xShift, yShift)
                    keep_in_box(name)
                else:
                    self._foxlastXvec[idx] = -self._foxlastXvec[idx]
                    self._foxlastYvec[idx] = -self._foxlastYvec[idx]
                    canv.move(name, self._foxlastXvec[idx], self._foxlastYvec[idx])
                    keep_in_box(name)
            self._job['move_free_fox'] = master.after(int(1 / START_SPEED), move_free_fox)

        def get_new_tail_pos():
            newX, newY = canv.coords('major')
            try:
                newX = self._xPath[(self._nFoxes) * TAIL_STEP_DISTANCE]
                newY = self._yPath[(self._nFoxes) * TAIL_STEP_DISTANCE]
                return (newX, newY)
            except IndexError:
                try:
                    if self._nFoxes:
                        newX, newY = canv.coords('tail' + str(self._nFoxes-1))
                except ValueError:
                    pass
            return (newX, newY)

        def keep_in_box(item):
            itemX, itemY = canv.coords(item)
            if itemX < BOX_X_MIN:
                canv.coords(item, BOX_X_MAX, itemY)
            if itemX > BOX_X_MAX:
                canv.coords(item, BOX_X_MIN, itemY)
            if itemY < BOX_Y_MIN:
                canv.coords(item, itemX, BOX_Y_MAX)
            if itemY > BOX_Y_MAX:
                canv.coords(item, itemX, BOX_Y_MIN)

        def move():
            if self._direction is not None:
                canv.move('major', self._xVelTumble, self._yVelTumble)
                itemX, itemY = canv.coords('major')
                self._xPath.appendleft(itemX)
                self._yPath.appendleft(itemY)
                keep_in_box('major')
                move_fox_tail()
                beerList = list(map(lambda x: 'beer' + str(x), range(N_BEERS)))
                freeFoxList = list(map(lambda x: 'fox' + str(x), range(N_FREE_FOXES)))
                # catch foxes
                foxCollision = check_clipping(itemX, itemY, include=freeFoxList)
                if foxCollision:
                    sound.play_sound(files.blopWav)
                    self._score += self._nBeers
                    self._nFoxes += 1
                    canv.itemconfig('foxText', text=': ' + str(self._nFoxes))
                    canv.itemconfig('starText', text=': ' + str(self._score))
                    newX, newY = get_new_tail_pos()
                    _draw_new_fox(newX=newX, newY=newY, name='tail' + str(self._nFoxes-1))
                    for item in reversed(itemRegister):
                        canv.tag_raise(item)
                    _draw_new_fox(name=foxCollision)
                    foxIdx = int(foxCollision.lstrip('fox'))
                    self._foxlastXvec[foxIdx] = random.random()
                    self._foxlastYvec[foxIdx] = random.random()
                    if not any(i in itemRegister for i in beerList):
                        for beerName in beerList:
                            if random.random() < BEER_RESPAWN_CHANCE:
                                _draw_new_beer(name=beerName)
                # drink beer
                beerCollision = check_clipping(itemX, itemY, include=beerList)
                if beerCollision:
                    sound.play_sound(files.slurpWav)
                    self._nBeers += 1
                    canv.itemconfig('beerText', text=': ' + str(self._nBeers) + ' / ' + str(MAX_BEER - 1))
                    canv.itemconfig('starText', text=': ' + str(self._score))
                    step = (MAX_SPEED - START_SPEED) / N_SPEED_STEPS
                    self._speed = min(self._speed + step, MAX_SPEED)
                    if self._nBeers == MAX_BEER - 1:
                        canv.itemconfig('eventInfoText', text=i18n.snakeEventInfo[i18n.lang()][1])
                    elif self._nBeers == MAX_BEER:
                        self._rotationSpeed = START_ROTATION_SPEED
                        canv.itemconfig('eventInfoText', text=i18n.snakeEventInfo[i18n.lang()][2])
                    elif self._nBeers > MAX_BEER:
                        step = (MAX_ROTATION_SPEED - START_ROTATION_SPEED) / N_ROTATION_SPEED_STEPS
                        self._rotationSpeed = min(self._rotationSpeed + step, MAX_ROTATION_SPEED)
                        step = (MAX_TUMBLE_ANGLE - START_TUMBLE_ANGLE) / N_TUMBLE_STEPS
                        self._tumbleAngle = min(self._tumbleAngle + step, MAX_TUMBLE_ANGLE)
                    if self._nBeers == MAX_BEER + 5:
                        _draw_new_bucket()
                        canv.itemconfig('eventInfoText', text=i18n.snakeEventInfo[i18n.lang()][4])
                    if random.random() < BEER_RESPAWN_CHANCE:
                        _draw_new_beer(name=beerCollision)
                    else:
                        delete_widget(beerCollision)
                # hit bucket
                if check_clipping(itemX, itemY, include='bucket'):
                    sound.play_sound(files.hiccupWav)
                    self._nBeers = MAX_BEER - 1
                    canv.itemconfig('beerText', text=': ' + str(self._nBeers) + ' / ' + str(MAX_BEER - 1))
                    delete_widget('bucket')
                    self._currentRotation = 0
                    self._rotationSpeed = 0
                    self._tumbleAngle = START_TUMBLE_ANGLE
                # rotate major and its direction
                # print('speed', self._speed, 'rotationSpeed', self._rotationSpeed, 'tumbleDegree', self._tumbleAngle)
                self._currentRotation += self._rotationSpeed
                canv.majorImg = ImageTk.PhotoImage(majorImgObj.rotate(self._tumbleAngle * 2 *
                                                                      math.sin(self._currentRotation)))
                canv.itemconfig('major', image=canv.majorImg)
                angle = maths.get_angle(1, 0, self._xVel, self._yVel)
                angle += self._tumbleAngle * math.sin(-self._currentRotation)
                angle = math.radians(angle)
                self._xVelTumble = MOVEMENT_STEP_SIZE * math.cos(angle)
                self._yVelTumble = MOVEMENT_STEP_SIZE * math.sin(angle)
                # check tail overlap
                noTailFoxes = [item for item in itemRegister if 'tail' not in item]
                noTailFoxes.extend(['tail' + str(idx) for idx in range(2)])
                crashFox = check_clipping(itemX, itemY, exclude=noTailFoxes,
                                          xSize=MAJOR_SIZE * 0.1,
                                          ySize=MAJOR_SIZE * 0.1)

                if crashFox:
                    sound.play_sound(files.blastWav)
                    print('Overlapping with tail', crashFox)
                    _end_game()
                    return
            self._job['move'] = master.after(int(1 / self._speed), move)

        def check_box_boundary(x, y, xSize=FOX_SIZE, ySize=FOX_SIZE):
            if x > BOX_X_MAX - xSize / 2 or \
               x < BOX_X_MIN + xSize / 2 or \
               y > BOX_Y_MAX - ySize / 2 or \
               y < BOX_Y_MIN + ySize / 2:
                return True

        def check_clipping(x, y, xSize=MAJOR_SIZE, ySize=MAJOR_SIZE, exclude=[], include=[]):
            for item in itemRegister:
                if item in exclude:
                    continue
                if include and item not in include:
                    continue
                itemX, itemY = canv.coords(item)
                x0, y0, x1, y1 = canv.bbox(item)
                itemSizeX = x1 - x0
                itemSizeY = y1 - y0
                # print('New item x/y', round(x), '/', round(y), item, itemX, '/', itemY)
                PROXIMITY = 3
                isCloseX = abs(itemX - x) < xSize / PROXIMITY + itemSizeX / PROXIMITY
                isCloseY = abs(itemY - y) < xSize / PROXIMITY + itemSizeY / PROXIMITY
                if isCloseX and isCloseY:
                    return item
            return ''

        def get_new_random_pos(xSize, ySize):
            nTries = 0
            while True:
                newX = BOX_X_MAX * random.random()
                newY = BOX_Y_MAX * random.random()
                # print(nTries, 'Trying newX newY', newX, '/', newY)
                if nTries > MAX_POSITION_LOOPS:
                    return (None, None)
                else:
                    nTries += 1
                if check_box_boundary(newX, newY, xSize, ySize):
                    continue
                if check_clipping(newX, newY, xSize, ySize):
                    continue
                return (newX, newY)

        def display_highscore():
            xCenter = self.infoBoxXMin + self.infoBoxWidth * 0.5
            xDistToEdge = 10
            canv.create_text(xCenter, BOX_Y_MIN + self.boxHeight * 0.5,
                             text='Loading highscore...', font='b', tags=('load_highscore'))
            scores = web_client.read_highscore()
            keys = None
            try:
                keys = sorted(scores[0].keys())
            except IndexError:
                canv.itemconfig('load_highscore', text='No data available')
            if keys:
                delete_widget('load_highscore')

                canv.create_text(xCenter, BOX_Y_MIN + 20,
                                 text='Global highscore list', font='b', tags=('global_highscore'))
                t = SimpleTable(master, N_HIGHSCORES + 1, len(keys))
                t.place(x=self.infoBoxXMin + xDistToEdge, y=BOX_Y_MIN + 40,
                        width=self.infoBoxWidth - 2 * xDistToEdge,
                        height=self.boxHeight * 0.4)
                t.headers(keys)
                t.data(scores, keys)

                canv.create_text(xCenter, BOX_Y_MIN + self.boxHeight * 0.5 + 20,
                                 text='Personal highscore list', font='b', tags=('personal_highscore'))
                canv.create_text(xCenter, BOX_Y_MIN + self.boxHeight * 0.75,
                                 text='Not available', font='b', tags=('no_personal_highscore'))

        def _init_start(event):
            reset(self)
            yPos = (BOX_Y_MAX + FULL_HEIGHT) / 2
            _draw_new_fox(BOX_X_MAX * 0.15, yPos, 'scoreFox', 0.5)
            canv.create_text(BOX_X_MAX * 0.25, yPos,
                             text=':' + str(self._nFoxes),
                             font='b', tags=('foxText'))
            _draw_new_beer(BOX_X_MAX * 0.45, yPos, 'scoreBeer', 0.5)
            canv.create_text(BOX_X_MAX * 0.55, yPos,
                             text=':' + str(self._nBeers) + ' / ' + str(MAX_BEER - 1),
                             font='b', tags=('beerText'))
            _draw_new_star(BOX_X_MAX * 0.75, yPos, 'scoreStar', 0.5)
            canv.create_text(BOX_X_MAX * 0.85, yPos,
                             text=':' + str(self._nBeers),
                             font='b', tags=('starText'))
            canv.create_text(BOX_X_MAX / 2, BOX_Y_MIN * 0.73, fill='red',
                             text=i18n.snakeEventInfo[i18n.lang()][0], tags=('eventInfoText'))
            _start(event)

        def _start(event):
            # delete_widget('welcomeText')
            delete_widget('instructionText')
            delete_widget('instructionText2')
            delete_widget('instrStar')
            delete_widget('instrBeer')
            delete_widget('instrFox')
            delete_widget('instructionEquals')
            delete_widget('instructionTimes')
            for idx in range(N_FREE_FOXES):
                _draw_new_fox(name='fox' + str(idx))
            for idx in range(N_BEERS):
                _draw_new_beer(name='beer' + str(idx))
            master.bind('<Up>', _change_direction)
            master.bind('<Down>', _change_direction)
            master.bind('<Right>', _change_direction)
            master.bind('<Left>', _change_direction)
            master.bind('w', _change_direction)
            master.bind('a', _change_direction)
            master.bind('s', _change_direction)
            master.bind('d', _change_direction)
            master.unbind('<Return>')
            move()
            move_free_fox()
            t1 = threading.Thread(target=display_highscore)
            t1.start()

        def _quit(self):
            time.sleep(0.1)
            master.quit()

        def _click_quit():
            _quit(self)

        def cancel():
            for job in self._job:
                master.after_cancel(self._job[job])
            self._job = {}

        def remove_items():
            # keepItems = ['scoreFox', 'scoreBeer', 'scoreStar']
            # for item in itemRegister:
            #     if item not in keepItems:
            #         canv.delete(item)
            pass

        def _end_game():
            cancel()
            remove_items()
            canv.itemconfig('eventInfoText', text='R.I.P.')
            canv.create_text(BOX_X_MAX / 2, BOX_Y_MIN + (BOX_Y_MAX - BOX_Y_MIN) * 0.5, fill='red', font='b',
                             text=i18n.gameOver[i18n.lang()][0], tags=('gameOverText'))
            canv.create_text(BOX_X_MAX / 2, BOX_Y_MIN + (BOX_Y_MAX - BOX_Y_MIN) * 0.6, fill='red',
                             text=i18n.gameOver[i18n.lang()][1], tags=('gameOverCancelText'))
            canv.create_text(BOX_X_MAX / 2, BOX_Y_MIN + (BOX_Y_MAX - BOX_Y_MIN) * 0.7, fill='red',
                             text=i18n.gameOver[i18n.lang()][2], tags=('gameOverRestartText'))
            master.bind('<Return>', _restart)

        def _restart(event):
            reset(self)
            delete_widget('gameOverText')
            delete_widget('gameOverCancelText')
            delete_widget('gameOverRestartText')
            delete_widget('bucket')
            tailFoxes = [item for item in itemRegister if 'tail' in item]
            for item in tailFoxes:
                delete_widget(item)
            canv.itemconfig('foxText', text=': ' + str(self._nFoxes))
            canv.itemconfig('beerText', text=': ' + str(self._nBeers) + ' / ' + str(MAX_BEER - 1))
            canv.itemconfig('starText', text=': ' + str(self._score))
            canv.itemconfig('eventInfoText', text=i18n.snakeEventInfo[i18n.lang()][0])
            canv.coords('major', BOX_X_MIN + self.boxWidth * 0.5, BOX_Y_MIN + (BOX_Y_MAX - BOX_Y_MIN) / 2)
            canv.majorImg = ImageTk.PhotoImage(majorImgObj.rotate(0))
            canv.itemconfig('major', image=canv.majorImg)
            _start(event)

        def _change_direction(event):
            if event.keysym == 'w':
                event.keysym = 'Up'
            if event.keysym == 'a':
                event.keysym = 'Left'
            if event.keysym == 's':
                event.keysym = 'Down'
            if event.keysym == 'd':
                event.keysym = 'Right'
            if not self._direction:
                canv.itemconfig('eventInfoText', text=i18n.snakeEventInfo[i18n.lang()][3])
            if not self._nFoxes:
                self._direction = 'measingless'
            if event.keysym == 'Up' and self._direction != 'Down':
                self._yVel = -MOVEMENT_STEP_SIZE
                self._xVel = 0
                self._direction = event.keysym
            if event.keysym == 'Down' and self._direction != 'Up':
                self._yVel = MOVEMENT_STEP_SIZE
                self._xVel = 0
                self._direction = event.keysym
            if event.keysym == 'Right' and self._direction != 'Left':
                self._yVel = 0
                self._xVel = MOVEMENT_STEP_SIZE
                self._direction = event.keysym
            if event.keysym == 'Left' and self._direction != 'Right':
                self._yVel = 0
                self._xVel = -MOVEMENT_STEP_SIZE
                self._direction = event.keysym

        master.protocol("WM_DELETE_WINDOW", _click_quit)
        master.bind('<Up>', _init_start)
        master.bind('<Down>', _init_start)
        master.bind('<Right>', _init_start)
        master.bind('<Left>', _init_start)
        master.bind('w', _init_start)
        master.bind('a', _init_start)
        master.bind('s', _init_start)
        master.bind('d', _init_start)
        master.bind('<Escape>', _quit)
        master.bind('<Return>', _init_start)


def main():
    print('Executing snake game!')
    root = tk.Tk()
    if sys.platform == 'win32':
        root.iconbitmap(files.foxIco)
    root.title(i18n.snakeWelcome[i18n.lang()])
    SnakeWindow(root)
    root.focus_force()
    root.mainloop()
    root.destroy()


if __name__ == '__main__':
    main()
