
import tkinter as tk

import gui
import i18n
import files


class SnakeWindow:

    def __init__(self, master):
        gui.center_window(master)
        master.protocol("WM_DELETE_WINDOW", master.quit)

        _OK_button = tk.Button(master, text=i18n.startButtonText[i18n.lang()][1], command=master.quit)
        _OK_button.grid(row=1, columnspan=3)

        def _quit(self):
            master.quit()

        master.bind('<Return>', _quit)
        master.bind('<Escape>', _quit)


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
