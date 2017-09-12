import math
import random
import time
from collections import deque

import tkinter as tk
from PIL import Image
from PIL import ImageTk

import files
import gui
import i18n

FULL_WIDTH = 400
FULL_HEIGHT = 450
BOX_X_MAX = 400
BOX_Y_MAX = 450
BOX_X_MIN = 0
BOX_Y_MIN = 50
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

START_SPEED = 1 / 50
MAX_SPEED = 4 / 50
N_SPEED_STEPS = 6

START_ROTATION_SPEED = 0.05
MAX_ROTATION_SPEED = 0.10
N_ROTATION_SPEED_STEPS = 10

START_TUMBLE_ANGLE = 5
MAX_TUMBLE_ANGLE = 45
N_TUMBLE_STEPS = 10

majorImgPath = files.resource_path('', r'images\major.png')
foxImgPath = files.resource_path('', r'images\fox.ico')
beerImgPath = files.resource_path('', r'images\beer.png')
starImgPath = files.resource_path('', r'images\star.png')
bucketImgPath = files.resource_path('', r'images\bucket.png')


def get_angle(x0, y0, x1, y1):
    mag0 = math.sqrt(x0**2 + y0**2)
    mag1 = math.sqrt(x1**2 + y1**2)
    if not mag0 or not mag1:
        return 0
    dot = x0 * x1 + y0 * y1
    det = x0 * y1 - x1 * y0
    angle = math.degrees(math.atan2(det, dot))
    return angle


class SnakeWindow:

    def __init__(self, master):
        gui.center_window(master)

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
            self._job = None
            self._rotationSpeed = 0
            self._currentRotation = 0
            self._tumbleAngle = START_TUMBLE_ANGLE
            self._foxlastXvec = random.random()
            self._foxlastYvec = random.random()

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

        majorImgObj = Image.open(majorImgPath)
        majorImgObj = majorImgObj.resize((MAJOR_SIZE, MAJOR_SIZE), Image.ANTIALIAS)
        canv.majorImg = ImageTk.PhotoImage(majorImgObj)

        foxImgObj = Image.open(foxImgPath)
        foxImgObj = foxImgObj.resize((FOX_SIZE, FOX_SIZE), Image.ANTIALIAS)

        beerImgObj = Image.open(beerImgPath)
        beerImgObj = beerImgObj.resize((BEER_SIZE, BEER_SIZE), Image.ANTIALIAS)

        starImgObj = Image.open(starImgPath)
        starImgObj = starImgObj.resize((STAR_SIZE, STAR_SIZE), Image.ANTIALIAS)

        bucketImgObj = Image.open(bucketImgPath)
        bucketImgObj = bucketImgObj.resize((BUCKET_SIZE, BUCKET_SIZE), Image.ANTIALIAS)

        canv.foxImg = {}
        canv.beerImg = {}
        canv.starImg = {}
        canv.bucketImg = {}

        canv.create_line(BOX_X_MIN, BOX_Y_MIN, BOX_X_MAX, BOX_Y_MIN, fill='black', tags=('top'), width=10)
        canv.create_line(BOX_X_MIN, BOX_Y_MIN, BOX_X_MIN, BOX_Y_MAX, fill='black', tags=('left'), width=10)
        canv.create_line(BOX_X_MAX - 1, BOX_Y_MIN, BOX_X_MAX - 1, BOX_Y_MAX, fill='black', tags=('right'), width=10)
        canv.create_line(BOX_X_MIN, BOX_Y_MAX - 2, BOX_X_MAX, BOX_Y_MAX - 2, fill='black', tags=('bottom'), width=10)

        canv.create_text(FULL_WIDTH / 2, BOX_Y_MIN * 0.4, text=i18n.snakeWelcome[i18n.lang()],
                         tags=('welcomeText'), font='b', fill='orange')
        canv.create_text(BOX_X_MAX / 2, BOX_Y_MAX * 2 / 8, text=i18n.snakeInstruction[i18n.lang()][0],
                         tags=('instructionText'))
        canv.create_text(FULL_WIDTH / 2, BOX_Y_MAX * 6 / 8, text=i18n.snakeInstruction[i18n.lang()][1],
                         tags=('instructionText2'))

        _draw_new_star(FULL_WIDTH * 0.30, BOX_Y_MAX * 0.9, "instrStar", 0.5)
        canv.create_text(FULL_WIDTH * 0.40, BOX_Y_MAX * 0.9, text='=', tags=('instructionEquals'))
        _draw_new_beer(FULL_WIDTH * 0.50, BOX_Y_MAX * 0.9, "instrBeer", 0.5)
        canv.create_text(FULL_WIDTH * 0.60, BOX_Y_MAX * 0.9, text='X', tags=('instructionTimes'))
        _draw_new_fox(FULL_WIDTH * 0.70, BOX_Y_MAX * 0.9, "instrFox", 0.5)

        canv.create_image(FULL_WIDTH / 2, BOX_Y_MIN + (BOX_Y_MAX - BOX_Y_MIN) / 2, image=canv.majorImg, tags=('major'))
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
            x, y = canv.coords('fox')
            while True:
                yShift = random.randint(-1, 1) * MOVEMENT_STEP_SIZE / 2
                xShift = random.randint(-1, 1) * MOVEMENT_STEP_SIZE / 2
                angle = get_angle(xShift, yShift, self._foxlastXvec, self._foxlastYvec)
                if abs(angle) < 60:
                    break
            self._foxlastXvec = xShift
            self._foxlastYvec = yShift
            x, y = x + xShift, y + yShift
            if check_clipping(x, y, xSize=FOX_SIZE, ySize=FOX_SIZE, exclude='fox'):
                return
            canv.move('fox', xShift, yShift)
            keep_in_box('fox')

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
                move_free_fox()
                # catch foxes
                if check_clipping(itemX, itemY, include='fox'):
                    self._score += self._nBeers
                    self._nFoxes += 1
                    canv.itemconfig('foxText', text=': ' + str(self._nFoxes))
                    canv.itemconfig('starText', text=': ' + str(self._score))
                    newX, newY = get_new_tail_pos()
                    _draw_new_fox(newX=newX, newY=newY, name='tail' + str(self._nFoxes-1))
                    for item in reversed(itemRegister):
                        canv.tag_raise(item)
                    _draw_new_fox()
                    self._foxlastXvec = random.random()
                    self._foxlastYvec = random.random()
                    if 'beer' not in itemRegister:
                        _draw_new_beer()
                # drink beer
                if check_clipping(itemX, itemY, include='beer'):
                    self._nBeers += 1
                    canv.itemconfig('beerText', text=': ' + str(self._nBeers))
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
                        _draw_new_beer()
                    else:
                        delete_widget('beer')
                # hit bucket
                if check_clipping(itemX, itemY, include='bucket'):
                    self._nBeers = MAX_BEER - 1
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
                angle = get_angle(1, 0, self._xVel, self._yVel)
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
                    print('Overlapping with tail', crashFox)
                    _end_game()
                    return
            self._job = master.after(int(1 / self._speed), move)

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

        def _init_start(event):
            reset(self)
            _draw_new_fox(BOX_X_MAX * 0.15, BOX_Y_MIN * 0.4, 'scoreFox', 0.5)
            canv.create_text(BOX_X_MAX * 0.25, BOX_Y_MIN * 0.4, text=':' + str(self._nFoxes),
                             font='b', tags=('foxText'))
            _draw_new_beer(BOX_X_MAX * 0.45, BOX_Y_MIN * 0.4, 'scoreBeer', 0.5)
            canv.create_text(BOX_X_MAX * 0.55, BOX_Y_MIN * 0.4, text=':' + str(self._nBeers),
                             font='b', tags=('beerText'))
            _draw_new_star(BOX_X_MAX * 0.75, BOX_Y_MIN * 0.4, 'scoreStar', 0.5)
            canv.create_text(BOX_X_MAX * 0.85, BOX_Y_MIN * 0.4, text=':' + str(self._nBeers),
                             font='b', tags=('starText'))
            canv.create_text(BOX_X_MAX / 2, BOX_Y_MIN * 0.73, fill='red',
                             text=i18n.snakeEventInfo[i18n.lang()][0], tags=('eventInfoText'))
            _start(event)

        def _start(event):
            delete_widget('welcomeText')
            delete_widget('instructionText')
            delete_widget('instructionText2')
            delete_widget('instrStar')
            delete_widget('instrBeer')
            delete_widget('instrFox')
            delete_widget('instructionEquals')
            delete_widget('instructionTimes')
            _draw_new_fox()
            _draw_new_beer()
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

        def _quit(self):
            time.sleep(0.1)
            master.quit()

        def _click_quit():
            _quit(self)

        def cancel():
            if self._job is not None:
                master.after_cancel(self._job)
                self._job = None

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
            canv.itemconfig('beerText', text=': ' + str(self._nBeers))
            canv.itemconfig('starText', text=': ' + str(self._score))
            canv.itemconfig('eventInfoText', text=i18n.snakeEventInfo[i18n.lang()][0])
            canv.coords('major', FULL_WIDTH / 2, BOX_Y_MIN + (BOX_Y_MAX - BOX_Y_MIN) / 2)
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


foxIco = files.resource_path('', r'images\fox.ico')


def main():
    print('Executing only snake!')
    root = tk.Tk()
    root.iconbitmap(foxIco)
    root.title(i18n.snakeWelcome[i18n.lang()])
    SnakeWindow(root)
    root.focus_force()
    root.mainloop()
    root.destroy()


if __name__ == '__main__':
    main()
