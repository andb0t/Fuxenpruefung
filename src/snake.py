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

FULL_WIDTH = 200
FULL_HEIGHT = 200
BOX_X_MAX = 200
BOX_Y_MAX = 200
BOX_X_MIN = 0
BOX_Y_MIN = 30
MAX_QUEUE_LEN = 1000
TAIL_STEP_DISTANCE = 6
STEP_SIZE = 5

MAJOR_SIZE = 70
FOX_SIZE = 40
BEER_SIZE = 40
N_MAX_LOOP = 10000

majorImgPath = files.resource_path('', r'images\fox.ico')
foxImgPath = files.resource_path('', r'images\fox.ico')
beerImgPath = files.resource_path('', r'images\beer.png')


class SnakeWindow:

    def __init__(self, master):
        gui.center_window(master)

        master.geometry('%sx%s+%s+%s' % (FULL_WIDTH, FULL_HEIGHT, 100, 100))
        master.resizable(0, 0)

        canv = tk.Canvas(master, highlightthickness=0)
        canv.pack(fill='both', expand=True)
        canv.create_line(BOX_X_MIN, BOX_Y_MIN, BOX_X_MAX, BOX_Y_MIN, fill='black', tags=('top'), width=10)
        canv.create_line(BOX_X_MIN, BOX_Y_MIN, BOX_X_MIN, BOX_Y_MAX, fill='black', tags=('left'), width=10)
        canv.create_line(BOX_X_MAX - 1, BOX_Y_MIN, BOX_X_MAX - 1, BOX_Y_MAX, fill='black', tags=('right'), width=10)
        canv.create_line(BOX_X_MIN, BOX_Y_MAX - 2, BOX_X_MAX, BOX_Y_MAX - 2, fill='black', tags=('bottom'), width=10)
        canv.create_text(FULL_WIDTH / 2, FULL_HEIGHT * 1 / 16, text=i18n.snakeWelcome[i18n.lang()],
                         tags=('welcomeText'), font='b', fill='orange')
        canv.create_text(BOX_X_MAX / 2, BOX_Y_MAX * 6 / 8, text=i18n.snakeInstruction[i18n.lang()][0],
                         tags=('instructionText'))
        canv.create_text(FULL_WIDTH / 2, BOX_Y_MAX * 7 / 8, text=i18n.snakeInstruction[i18n.lang()][1],
                         tags=('instructionText2'))

        itemRegister = []
        self._xPath = deque([], MAX_QUEUE_LEN)
        self._yPath = deque([], MAX_QUEUE_LEN)
        self._xVel = 0
        self._yVel = 0
        self._direction = None
        self._score = 0
        self._nFoxes = 0
        self._speed = 50
        gameStarted = False
        gameStopped = False

        majorImgObj = Image.open(majorImgPath)
        majorImgObj = majorImgObj.resize((MAJOR_SIZE, MAJOR_SIZE), Image.ANTIALIAS)
        canv.majorImg = ImageTk.PhotoImage(majorImgObj)

        foxImgObj = Image.open(foxImgPath)
        foxImgObj = foxImgObj.resize((FOX_SIZE, FOX_SIZE), Image.ANTIALIAS)
        canv.foxImg = ImageTk.PhotoImage(foxImgObj)

        beerImgObj = Image.open(beerImgPath)
        beerImgObj = beerImgObj.resize((BEER_SIZE, BEER_SIZE), Image.ANTIALIAS)
        canv.beerImg = ImageTk.PhotoImage(beerImgObj)

        canv.create_image(FULL_WIDTH / 2, FULL_HEIGHT / 2, image=canv.majorImg, tags=('major'))
        itemRegister.append('major')

        print(canv.coords('major'))

        def move_fox_tail():
            for idx in range(self._nFoxes):
                thisFoxTag = 'tail' + str(idx)
                try:
                    canv.coords(thisFoxTag,
                                self._xPath[(idx + 1) * TAIL_STEP_DISTANCE],
                                self._yPath[(idx + 1) * TAIL_STEP_DISTANCE])
                except IndexError:
                    pass

        def get_new_fox_pos():
            newX, newY = canv.coords('major')
            try:
                newX = self._xPath[(self._nFoxes + 1) * TAIL_STEP_DISTANCE]
                newY = self._yPath[(self._nFoxes + 1) * TAIL_STEP_DISTANCE]
                return (newX, newY)
            except IndexError:
                if self._nFoxes:
                    newX, newY = canv.coords('tail' + str(self._nFoxes))
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
                canv.move('major', self._xVel, self._yVel)
                itemX, itemY = canv.coords('major')
                self._xPath.appendleft(itemX)
                self._yPath.appendleft(itemY)
                keep_in_box('major')
                move_fox_tail()
                if check_clipping(itemX, itemY, include='fox'):
                    self._score += 1
                    canv.itemconfig('scoreText', text=i18n.snakeScore[i18n.lang()] + ': ' + str(self._score))
                    newX, newY = get_new_fox_pos()
                    _draw_new_fox(newX=newX, newY=newY, name='tail' + str(self._nFoxes))
                    for item in reversed(itemRegister):
                        canv.tag_raise(item)
                    self._nFoxes += 1
                    _draw_new_fox()
                if check_clipping(itemX, itemY, include='beer'):
                    _draw_new_beer()
                    self._speed = math.ceil(self._speed * 0.9)
            if not gameStopped:
                master.after(self._speed, move)

        def check_box_boundary(x, y, xSize=FOX_SIZE, ySize=FOX_SIZE):
            if x > BOX_X_MAX - xSize / 2 or \
               x < BOX_X_MIN + xSize / 2 or \
               y > BOX_Y_MAX - ySize / 2 or \
               y < BOX_Y_MIN + ySize / 2:
                return True

        def check_clipping(x, y, xSize=FOX_SIZE, ySize=FOX_SIZE, exclude=[], include=[]):
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
                PROXIMITY = 2
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
                print(nTries, 'Trying newX newY', newX, '/', newY)
                if nTries > N_MAX_LOOP:
                    return (None, None)
                else:
                    nTries += 1
                if check_box_boundary(newX, newY, xSize, ySize):
                    continue
                if check_clipping(newX, newY, xSize, ySize):
                    continue
                return (newX, newY)

        def _draw_new_fox(newX=None, newY=None, name='fox'):
            if not newX and not newY:
                newX, newY = get_new_random_pos(FOX_SIZE, FOX_SIZE)
                if not newX and not newY:
                    _end_game()
            canv.delete(name)
            canv.create_image(newX, newY, image=canv.foxImg, tags=(name))
            itemRegister.append(name)

        def _draw_new_beer(newX=None, newY=None, name='beer'):
            if not newX and not newY:
                newX, newY = get_new_random_pos(BEER_SIZE, BEER_SIZE)
                if not newX and not newY:
                    _end_game()
            canv.delete(name)
            canv.create_image(newX, newY, image=canv.beerImg, tags=(name))
            itemRegister.append(name)

        def _start(event):
            global gameStarted
            canv.delete('welcomeText')
            canv.delete('instructionText')
            canv.delete('instructionText2')
            _draw_new_fox()
            _draw_new_beer()
            print('Start the game')
            gameStarted = True
            master.bind('<Up>', _go_direction)
            master.bind('<Down>', _go_direction)
            master.bind('<Right>', _go_direction)
            master.bind('<Left>', _go_direction)
            master.unbind('<Return>')
            canv.create_text(BOX_X_MAX / 2, FULL_HEIGHT * 1 / 16,
                             text=i18n.snakeScore[i18n.lang()] + ': '+str(self._score), tags=('scoreText'))
            move()

        def _quit(self):
            global gameStopped
            gameStopped = True
            time.sleep(0.1)
            master.quit()

        def _end_game():
            _quit(self)

        def _go_direction(event):
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

        master.protocol("WM_DELETE_WINDOW", _quit)
        master.bind('<Up>', _start)
        master.bind('<Down>', _start)
        master.bind('<Right>', _start)
        master.bind('<Left>', _start)
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
