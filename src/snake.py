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

FULL_WIDTH = 300
FULL_HEIGHT = 300
BOX_X_MAX = 300
BOX_Y_MAX = 300
BOX_X_MIN = 0
BOX_Y_MIN = 30
MAX_QUEUE_LEN = 1000
TAIL_STEP_DISTANCE = 6
STEP_SIZE = 5

MAJOR_SIZE = 80
FOX_SIZE = 40
BEER_SIZE = 40
STAR_SIZE = 40
N_MAX_LOOP = 10000
MAX_SPEED = 5 / 50
START_SPEED = 1 / 50
SPEED_STEPS = 1
ROTATION_SPEED_STEP = 0.01
MAX_DIR_CHANGE = 120  # allow only direction changes up to this angle
MAX_TUMBLE = 45
MAX_TUMBLE_MOVE = 20

majorImgPath = files.resource_path('', r'images\major.png')
foxImgPath = files.resource_path('', r'images\fox.ico')
beerImgPath = files.resource_path('', r'images\beer.png')
starImgPath = files.resource_path('', r'images\star.png')


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
        gameStarted = False
        gameStopped = False

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

        canv.foxImg = {}
        canv.beerImg = {}
        canv.starImg = {}

        canv.create_line(BOX_X_MIN, BOX_Y_MIN, BOX_X_MAX, BOX_Y_MIN, fill='black', tags=('top'), width=10)
        canv.create_line(BOX_X_MIN, BOX_Y_MIN, BOX_X_MIN, BOX_Y_MAX, fill='black', tags=('left'), width=10)
        canv.create_line(BOX_X_MAX - 1, BOX_Y_MIN, BOX_X_MAX - 1, BOX_Y_MAX, fill='black', tags=('right'), width=10)
        canv.create_line(BOX_X_MIN, BOX_Y_MAX - 2, BOX_X_MAX, BOX_Y_MAX - 2, fill='black', tags=('bottom'), width=10)
        canv.create_text(FULL_WIDTH / 2, BOX_Y_MIN / 2, text=i18n.snakeWelcome[i18n.lang()],
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

        canv.create_image(FULL_WIDTH / 2, FULL_HEIGHT / 2, image=canv.majorImg, tags=('major'))
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
                # drink beer
                if check_clipping(itemX, itemY, include='beer'):
                    if self._speed == MAX_SPEED:
                        self._rotationSpeed += ROTATION_SPEED_STEP
                    self._nBeers += 1
                    canv.itemconfig('beerText', text=': ' + str(self._nBeers))
                    canv.itemconfig('starText', text=': ' + str(self._score))
                    self._speed = min(self._speed + (MAX_SPEED - START_SPEED) / SPEED_STEPS, MAX_SPEED)
                    _draw_new_beer()
                # rotate major and its direction
                self._currentRotation += self._rotationSpeed
                canv.majorImg = ImageTk.PhotoImage(majorImgObj.rotate(MAX_TUMBLE * math.sin(self._currentRotation)))
                canv.itemconfig('major', image=canv.majorImg)
                angle = get_angle(1, 0, self._xVel, self._yVel)
                angle += MAX_TUMBLE_MOVE * math.sin(self._currentRotation)
                angle = math.radians(angle)
                self._xVelTumble = STEP_SIZE * math.cos(angle)
                self._yVelTumble = STEP_SIZE * math.sin(angle)
                # check tail overlap
                noTailFoxes = [item for item in itemRegister if 'tail' not in item]
                noTailFoxes.extend(['tail' + str(idx) for idx in range(2)])
                if check_clipping(itemX, itemY, exclude=noTailFoxes):
                    print('Overlapping with own tail!')
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
                    return True
            return False

        def get_new_random_pos(xSize, ySize):
            nTries = 0
            while True:
                newX = BOX_X_MAX * random.random()
                newY = BOX_Y_MAX * random.random()
                # print(nTries, 'Trying newX newY', newX, '/', newY)
                if nTries > N_MAX_LOOP:
                    return (None, None)
                else:
                    nTries += 1
                if check_box_boundary(newX, newY, xSize, ySize):
                    continue
                if check_clipping(newX, newY, xSize, ySize):
                    continue
                return (newX, newY)

        def _start(event):
            global gameStarted
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
            gameStarted = True
            master.bind('<Up>', _change_direction)
            master.bind('<Down>', _change_direction)
            master.bind('<Right>', _change_direction)
            master.bind('<Left>', _change_direction)
            master.bind('w', _change_direction)
            master.bind('a', _change_direction)
            master.bind('s', _change_direction)
            master.bind('d', _change_direction)
            master.unbind('<Return>')
            _draw_new_fox(BOX_X_MAX * 0.15, FULL_HEIGHT * 0.05, 'scoreFox', 0.5)
            canv.create_text(BOX_X_MAX * 0.25, FULL_HEIGHT * 0.05, text=':' + str(self._nFoxes),
                             font='b', tags=('foxText'))
            _draw_new_beer(BOX_X_MAX * 0.45, FULL_HEIGHT * 0.05, 'scoreBeer', 0.5)
            canv.create_text(BOX_X_MAX * 0.55, FULL_HEIGHT * 0.05, text=':' + str(self._nBeers),
                             font='b', tags=('beerText'))
            _draw_new_star(BOX_X_MAX * 0.75, FULL_HEIGHT * 0.05, 'scoreStar', 0.5)
            canv.create_text(BOX_X_MAX * 0.85, FULL_HEIGHT * 0.05, text=':' + str(self._nBeers),
                             font='b', tags=('starText'))
            move()

        def _quit(self):
            global gameStopped
            gameStopped = True
            time.sleep(0.1)
            master.quit()

        def _click_quit():
            _quit(self)

        def cancel():
            if self._job is not None:
                master.after_cancel(self._job)
                self._job = None

        def remove_items():
            keepItems = ['scoreFox', 'scoreBeer', 'scoreStar']
            for item in itemRegister:
                if item not in keepItems:
                    canv.delete(item)

        def _end_game():
            cancel()
            remove_items()
            canv.create_text(BOX_X_MAX / 2, FULL_HEIGHT * 4 / 8, fill='red', font='b',
                             text=i18n.gameOver[i18n.lang()][0], tags=('gameOverText'))
            canv.create_text(BOX_X_MAX / 2, FULL_HEIGHT * 5 / 8, fill='red',
                             text=i18n.gameOver[i18n.lang()][1], tags=('gameOverInstructionText'))

        def _change_direction(event):
            if event.keysym == 'w':
                event.keysym = 'Up'
            if event.keysym == 'a':
                event.keysym = 'Left'
            if event.keysym == 's':
                event.keysym = 'Down'
            if event.keysym == 'd':
                event.keysym = 'Right'
            if event.keysym == 'Up' and self._direction != 'Down':
                self._yVel = -STEP_SIZE
                self._xVel = 0
                self._direction = event.keysym
            if event.keysym == 'Down' and self._direction != 'Up':
                self._yVel = STEP_SIZE
                self._xVel = 0
                self._direction = event.keysym
            if event.keysym == 'Right' and self._direction != 'Left':
                self._yVel = 0
                self._xVel = STEP_SIZE
                self._direction = event.keysym
            if event.keysym == 'Left' and self._direction != 'Right':
                self._yVel = 0
                self._xVel = -STEP_SIZE
                self._direction = event.keysym

        master.protocol("WM_DELETE_WINDOW", _click_quit)
        master.bind('<Up>', _start)
        master.bind('<Down>', _start)
        master.bind('<Right>', _start)
        master.bind('<Left>', _start)
        master.bind('w', _start)
        master.bind('a', _start)
        master.bind('s', _start)
        master.bind('d', _start)
        master.bind('<Escape>', _quit)
        master.bind('<Return>', _start)


foxIco = files.resource_path('', r'images\fox.ico')


def main():
    print('Executing only snake!')
    root = tk.Tk()
    root.iconbitmap(foxIco)
    root.title('Fox snake game')
    SnakeWindow(root)
    root.focus_force()
    root.mainloop()
    root.destroy()


if __name__ == '__main__':
    main()
