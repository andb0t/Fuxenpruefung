import random

import tkinter as tk
from PIL import Image
from PIL import ImageTk

import gui
import i18n
import files

FULL_WIDTH = 600
FULL_HEIGHT = 600

majorImgPath = files.resource_path('', r'images\fox.ico')


class SnakeWindow:

    def __init__(self, master):
        gui.center_window(master)

        master.geometry('%sx%s+%s+%s' % (FULL_WIDTH, FULL_HEIGHT, 100, 100))
        master.resizable(0, 0)

        canv = tk.Canvas(master, highlightthickness=0)
        canv.pack(fill='both', expand=True)
        top = canv.create_line(0, 0, FULL_WIDTH, 0, fill='black', tags=('top'), width=10)
        left = canv.create_line(0, 0, 0, FULL_HEIGHT, fill='black', tags=('left'), width=10)
        right = canv.create_line(FULL_WIDTH - 1, 0, FULL_WIDTH - 1, FULL_HEIGHT, fill='black', tags=('right'), width=10)
        bottom = canv.create_line(0, FULL_HEIGHT - 2, FULL_WIDTH, FULL_HEIGHT - 2, fill='black', tags=('bottom'), width=10)

        majorImgObj = Image.open(majorImgPath)
        majorImgObj = majorImgObj.resize((30, 30), Image.ANTIALIAS)
        canv.majorImg = ImageTk.PhotoImage(majorImgObj, width=20)
        major = canv.create_image(FULL_WIDTH / 2, FULL_HEIGHT / 2, image=canv.majorImg, tags=('major'))

        def _draw_new_fox():
            newX = FULL_WIDTH * (0.05 + random.random() * 0.9)
            newY = FULL_HEIGHT * (0.05 + random.random() * 0.9)
            canv.delete('fox')
            self.fox = canv.create_image(newX, newY, image=canv.majorImg, tags=('fox'))

        def _start():
            _draw_new_fox()
            print('Start the game')

        def _quit():
            master.quit()

        def _start_bind(self):
            _start()

        def _quit_bind(self):
            _quit()

        master.protocol("WM_DELETE_WINDOW", _quit)
        master.bind('<Return>', _start_bind)
        master.bind('<Escape>', _quit_bind)


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
