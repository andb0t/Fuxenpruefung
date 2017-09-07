import random

import tkinter as tk
from PIL import Image
from PIL import ImageTk

import gui
import i18n
import files

FULL_WIDTH = 200
FULL_HEIGHT = 200
BOX_WIDTH = 200
BOX_HEIGHT = 200
BOX_X_MIN = 0
BOX_Y_MIN = 30

MAJOR_SIZE = 70
FOX_SIZE = 40
N_MAX_LOOP = 100000

majorImgPath = files.resource_path('', r'images\fox.ico')
foxImgPath = files.resource_path('', r'images\fox.ico')


class SnakeWindow:

    def __init__(self, master):
        gui.center_window(master)

        master.geometry('%sx%s+%s+%s' % (FULL_WIDTH, FULL_HEIGHT, 100, 100))
        master.resizable(0, 0)

        canv = tk.Canvas(master, highlightthickness=0)
        canv.pack(fill='both', expand=True)
        canv.create_line(BOX_X_MIN, BOX_Y_MIN, BOX_WIDTH, BOX_Y_MIN, fill='black', tags=('top'), width=10)
        canv.create_line(BOX_X_MIN, BOX_Y_MIN, BOX_X_MIN, BOX_HEIGHT, fill='black', tags=('left'), width=10)
        canv.create_line(BOX_WIDTH - 1, BOX_Y_MIN, BOX_WIDTH - 1, BOX_HEIGHT, fill='black', tags=('right'), width=10)
        canv.create_line(BOX_X_MIN, BOX_HEIGHT - 2, BOX_WIDTH, BOX_HEIGHT - 2, fill='black', tags=('bottom'), width=10)
        canv.create_text(BOX_WIDTH / 2, BOX_HEIGHT * 1 / 16, text=i18n.snakeWelcome[i18n.lang()],
                         tags=('welcomeText'), font='b', fill='orange')
        canv.create_text(BOX_WIDTH / 2, BOX_HEIGHT * 6 / 8, text=i18n.snakeInstruction[i18n.lang()][0],
                         tags=('instructionText'))
        canv.create_text(FULL_WIDTH / 2, FULL_HEIGHT * 7 / 8, text=i18n.snakeInstruction[i18n.lang()][1],
                         tags=('instructionText2'))

        itemRegister = []
        self._xVel = 0
        self._yVel = 0
        self._direction = None
        self._score = 0
        gameStarted = False

        majorImgObj = Image.open(majorImgPath)
        majorImgObj = majorImgObj.resize((MAJOR_SIZE, MAJOR_SIZE), Image.ANTIALIAS)
        canv.majorImg = ImageTk.PhotoImage(majorImgObj)

        foxImgObj = Image.open(foxImgPath)
        foxImgObj = foxImgObj.resize((FOX_SIZE, FOX_SIZE), Image.ANTIALIAS)
        canv.foxImg = ImageTk.PhotoImage(foxImgObj)

        major = canv.create_image(FULL_WIDTH / 2, FULL_HEIGHT / 2, image=canv.majorImg, tags=('major'))
        itemRegister.append('major')

        print(canv.coords('major'))

        def keep_in_box(item):
            itemX, itemY = canv.coords(item)
            if itemX < 0:
                canv.coords(item, BOX_WIDTH, itemY)
            if itemX > BOX_WIDTH:
                canv.coords(item, 0, itemY)
            if itemY < 0:
                canv.coords(item, itemX, BOX_HEIGHT)
            if itemY > BOX_HEIGHT:
                canv.coords(item, itemX, 0)

        def move():
            if self._direction is not None:
                canv.move(major, self._xVel, self._yVel)
                itemX, itemY = canv.coords(major)
                keep_in_box(major)
                if check_clipping(itemX, itemY, exclude='major'):
                    _draw_new_fox()
                    self._score += 1
                    canv.itemconfig('scoreText', text=i18n.snakeScore[i18n.lang()] + ': ' + str(self._score))
            master.after(50, move)

        def check_box_boundary(x, y, xSize=FOX_SIZE, ySize=FOX_SIZE):
            if x > BOX_WIDTH - xSize / 2 or \
               x < xSize / 2 or \
               y > BOX_HEIGHT - ySize / 2 or \
               y < ySize / 2:
                return True

        def check_clipping(x, y, xSize=FOX_SIZE, ySize=FOX_SIZE, exclude=[]):
            for item in itemRegister:
                if item in exclude:
                    continue
                itemX, itemY = canv.coords(item)
                x0, y0, x1, y1 = canv.bbox(item)  # returns a tuple like (x1, y1, x2, y2)
                itemSizeX = x1 - x0
                itemSizeY = y1 - y0
                # print('New item x/y', round(x), '/', round(y), item, itemX, '/', itemY)
                PROXIMITY = 4
                isCloseX = abs(itemX - x) < xSize / PROXIMITY + itemSizeX / PROXIMITY
                isCloseY = abs(itemY - y) < xSize / PROXIMITY + itemSizeY / PROXIMITY
                if isCloseX and isCloseY:
                    return True
            return False

        def get_new_random_pos(xSize, ySize):
            nTries = 0
            while True:
                newX = BOX_WIDTH * random.random()
                newY = BOX_HEIGHT * random.random()
                if nTries > N_MAX_LOOP:
                    return None
                if check_box_boundary(newX, newY, xSize, ySize):
                    continue
                if check_clipping(newX, newY, xSize, ySize):
                    continue
                return (newX, newY)

        def _draw_new_fox():
            newX, newY = get_new_random_pos(FOX_SIZE, FOX_SIZE)
            canv.delete('fox')
            canv.create_image(newX, newY, image=canv.foxImg, tags=('fox'))
            itemRegister.append('fox')

        def _start(event):
            global gameStarted
            canv.delete('welcomeText')
            canv.delete('instructionText')
            canv.delete('instructionText2')
            _draw_new_fox()
            print('Start the game')
            gameStarted = True
            master.bind('<Up>', _go_direction)
            master.bind('<Down>', _go_direction)
            master.bind('<Right>', _go_direction)
            master.bind('<Left>', _go_direction)
            canv.create_text(BOX_WIDTH / 2, BOX_HEIGHT * 1 / 16, text=i18n.snakeScore[i18n.lang()] + ': '+str(self._score),
                             tags=('scoreText'))
            move()

        def _quit(self):
            master.quit()

        def _go_direction(event):
            self._direction = event.keysym
            if self._direction == 'Up':
                self._yVel = -5
                self._xVel = 0
            if self._direction == 'Down':
                self._yVel = 5
                self._xVel = 0
            if self._direction == 'Right':
                self._yVel = 0
                self._xVel = 5
            if self._direction == 'Left':
                self._yVel = 0
                self._xVel = -5

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
    root.title('Foxnake game')
    SnakeWindow(root)
    root.focus_force()
    root.mainloop()
    root.destroy()


if __name__ == '__main__':
    main()
