import random

import tkinter as tk
from PIL import Image
from PIL import ImageTk

import gui
import i18n
import files

FULL_WIDTH = 200
FULL_HEIGHT = 200
FOX_SIZE = 70
N_MAX_LOOP = 100000

majorImgPath = files.resource_path('', r'images\fox.ico')


class SnakeWindow:

    def __init__(self, master):
        gui.center_window(master)

        master.geometry('%sx%s+%s+%s' % (FULL_WIDTH, FULL_HEIGHT, 100, 100))
        master.resizable(0, 0)

        canv = tk.Canvas(master, highlightthickness=0)
        canv.pack(fill='both', expand=True)
        canv.create_line(0, 0, FULL_WIDTH, 0, fill='black', tags=('top'), width=10)
        canv.create_line(0, 0, 0, FULL_HEIGHT, fill='black', tags=('left'), width=10)
        canv.create_line(FULL_WIDTH - 1, 0, FULL_WIDTH - 1, FULL_HEIGHT, fill='black', tags=('right'), width=10)
        canv.create_line(0, FULL_HEIGHT - 2, FULL_WIDTH, FULL_HEIGHT - 2, fill='black', tags=('bottom'), width=10)

        canv.create_text(FULL_WIDTH / 2, FULL_HEIGHT * 1 / 8, text=i18n.snakeWelcome[i18n.lang()],
                         tags=('welcomeText'), font='b', fill='orange')
        canv.create_text(FULL_WIDTH / 2, FULL_HEIGHT * 6 / 8, text=i18n.snakeInstruction[i18n.lang()][0],
                         tags=('instructionText'))
        canv.create_text(FULL_WIDTH / 2, FULL_HEIGHT * 7 / 8, text=i18n.snakeInstruction[i18n.lang()][1],
                         tags=('instructionText2'))

        itemRegister = {}

        majorImgObj = Image.open(majorImgPath)
        majorImgObj = majorImgObj.resize((FOX_SIZE, FOX_SIZE), Image.ANTIALIAS)
        canv.majorImg = ImageTk.PhotoImage(majorImgObj)
        major = canv.create_image(FULL_WIDTH / 2, FULL_HEIGHT / 2, image=canv.majorImg, tags=('major'))
        itemRegister['major'] = major

        print(canv.coords(itemRegister['major']))

        def check_clipping(x, y, xSize, ySize):
            if x > FULL_WIDTH - xSize / 2 or \
               x < xSize / 2 or \
               y > FULL_HEIGHT - ySize / 2 or \
               y < ySize / 2:
                return True
            for item in itemRegister.keys():
                itemX, itemY = canv.coords(itemRegister[item])
                itemSize = FOX_SIZE
                print('New item x/y', round(x), '/', round(y), item, itemX, '/', itemY)
                PROXIMITY = 4
                if abs(itemX - x) < xSize / PROXIMITY + itemSize / PROXIMITY or \
                   abs(itemY - y) < xSize / PROXIMITY + itemSize / PROXIMITY:
                    return True
            return False

        def get_new_random_pos(xSize, ySize):
            nTries = 0
            while True:
                newX = FULL_WIDTH * random.random()
                newY = FULL_HEIGHT * random.random()
                if nTries > N_MAX_LOOP:
                    return None
                if check_clipping(newX, newY, xSize, ySize):
                    continue
                return (newX, newY)

        def _draw_new_fox(self):
            newX, newY = get_new_random_pos(FOX_SIZE, FOX_SIZE)
            canv.delete('fox')
            self.fox = canv.create_image(newX, newY, image=canv.majorImg, tags=('fox'))

        def _start(self):
            canv.delete('welcomeText')
            canv.delete('instructionText')
            canv.delete('instructionText2')
            _draw_new_fox(self)
            print('Start the game')
            # master.bind('<Up>', _go_up_bind)
            # master.bind('<Down>', _go_down_bind)
            # master.bind('<Right>', _go_right_bind)
            # master.bind('<Left>', _go_left_bind)

        def _quit(self):
            master.quit()

        master.protocol("WM_DELETE_WINDOW", _quit)
        master.bind('<Up>', _start)
        master.bind('<Down>', _start)
        master.bind('<Right>', _start)
        master.bind('<Left>', _start)
        master.bind('<Escape>', _quit)
        master.bind('<Return>', _draw_new_fox)


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
