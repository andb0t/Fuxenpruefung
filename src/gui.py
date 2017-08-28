import sys
import webbrowser

import tkinter as tk

import i18n


def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func


def callback_GitHub(event):
    webbrowser.open_new(r"https://github.com/andb0t/Fuxenpruefung/releases")


def callback_AGV(event):
    webbrowser.open_new(r"http://agv-muenchen.de/")


def center_window(root, xdist=0, ydist=0):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # calculate position x and y coordinates
    x = (screen_width*xdist)
    y = (screen_height*ydist)
    root.geometry('+%d+%d' % (x, y))


class InitWindow:

    def __init__(self, master, categories, lang, pngList, radioinit=0):

        center_window(master)

        master.protocol("WM_DELETE_WINDOW", sys.exit)

        self.inputDict = {}
        self.radio_var = tk.IntVar()
        self.reinit = tk.IntVar()
        self.switch_lang = tk.IntVar()
        self.toggle_sound = tk.IntVar()

        self.reinit.set(0)
        self.switch_lang.set(0)
        self.toggle_sound.set(0)

        _row_count = 0

        _head_label = tk.Label(master, text=i18n.appHeader[lang], font=("Helvetica", 16))
        _head_label.grid(row=_row_count, columnspan=4)
        _row_count += 1

        _photo = tk.PhotoImage(file=pngList[0])
        _photo = _photo.subsample(5, 5)
        _photo_label = tk.Label(master, image=_photo)
        _photo_label.photo = _photo
        _photo_label.grid(row=_row_count, columnspan=4)
        _row_count += 1

        _col_idx = 0
        _row_count += 2
        for default, longName, shortName in categories:
            if shortName == 'P' or shortName == 'A':
                continue
            cat_label = tk.Label(master, text=longName)
            cat_label.grid(row=_row_count-2, column=_col_idx+1)
            string_val = tk.StringVar()
            string_val.set(default)
            cat_entry = tk.Entry(master, textvariable=string_val, width=5)
            cat_entry.grid(row=_row_count-1, column=_col_idx+1)
            self.inputDict[shortName] = string_val
            _col_idx = (_col_idx + 1) % 2
            if (_col_idx == 0):
                _row_count += 2

        for idx, task in enumerate(i18n.dictInit[lang]):
            rad = tk.Radiobutton(master, text=task, variable=self.radio_var, value=idx)
            rad.grid(row=_row_count, columnspan=4)
            _row_count += 1
        self.radio_var.set(radioinit)

        _start_button = tk.Button(master, text=i18n.startButtonText[lang][0],
                                  fg="green", font="bold", command=master.quit)
        _start_button.grid(row=_row_count, column=0, columnspan=2)
        _quit_button = tk.Button(master, text=i18n.startButtonText[lang][1],
                                 fg="red", font="bold", command=sys.exit)
        _quit_button.grid(row=_row_count, column=2, columnspan=2)
        _row_count += 1

        def set_reinit():
            self.reinit.set(1)

        def set_switch_lang():
            self.switch_lang.set(1)

        def set_toggle_sound():
            self.toggle_sound.set(1)

        _lang_button = tk.Button(master, command=combine_funcs(set_switch_lang, master.quit, set_reinit))
        _lang_button_image = tk.PhotoImage(file=pngList[1])
        # _lang_button_image = _lang_button_image.subsample(1, 1)
        _lang_button.config(image=_lang_button_image, width=30, height=20)
        _lang_button._lang_button_image = _lang_button_image
        _lang_button.grid(row=_row_count, column=0)

        _github_button = tk.Button(master)
        _github_button_image = tk.PhotoImage(file=pngList[2])
        _github_button_image = _github_button_image.subsample(7, 7)
        _github_button.config(image=_github_button_image, width=60, height=20)
        _github_button._github_button_image = _github_button_image
        _github_button.bind("<Button-1>", callback_GitHub)
        _github_button.grid(row=_row_count, column=3)

        _sound_button = tk.Button(master, command=combine_funcs(set_toggle_sound, master.quit, set_reinit))
        _sound_button_image = tk.PhotoImage(file=pngList[3])
        _sound_button_image = _sound_button_image.subsample(4, 4)
        _sound_button.config(image=_sound_button_image, height=20)
        _sound_button._sound_button_image = _sound_button_image
        _sound_button.grid(row=_row_count, column=1)

        _link_label = tk.Label(master, text=i18n.linkLabelText[lang], fg="blue", cursor="hand2")
        _link_label.grid(row=_row_count, column=2)
        _link_label.bind("<Button-1>", callback_AGV)

        thisradio = self.radio_var

        def _toggleup(self):
            old = thisradio.get()
            new = max(old - 1, 0)
            thisradio.set(new)

        def _toggledown(self):
            old = thisradio.get()
            new = min(old + 1, len(i18n.dictInit[lang])-1)
            thisradio.set(new)

        def _quit(self):
            master.quit()
        master.bind('<Escape>', sys.exit)
        master.bind('<Up>', _toggleup)
        master.bind('<Down>',  _toggledown)
        master.bind('<Return>', _quit)


class InfoWindow:

    def __init__(self, master, lines):

        center_window(master)

        master.protocol("WM_DELETE_WINDOW", master.quit)

        _row_count = 0
        _col_count = 0
        _widths = (200, 50, 50)
        _stickys = (tk.W, None, None)
        for line in lines:
            if isinstance(line, str):
                one_msg = tk.Message(master, text=line, width=200)
                one_msg.grid(row=_row_count, columnspan=3)
            elif isinstance(line, list) or isinstance(line, tuple):
                _col_count = 0
                for item in line:
                    multi_msg = tk.Message(master, text=line[_col_count],
                                           width=_widths[_col_count])
                    multi_msg.grid(row=_row_count, column=_col_count,
                                   sticky=_stickys[_col_count])
                    _col_count += 1
            _row_count += 1

        _OK_button = tk.Button(master, text="OK", command=master.quit)
        _OK_button.grid(row=_row_count, columnspan=3)

        def _quit(self):
            master.quit()
        master.bind('<Return>', _quit)
        master.bind('<Escape>', _quit)


def sticky_gen(count):
    if count > 0:
        return tk.W


class TextWindow:

    def __init__(self, master, header, lines):

        center_window(master)

        master.protocol("WM_DELETE_WINDOW", master.quit)

        _head_label = tk.Label(master, text=header)
        _head_label.pack(side=tk.TOP)

        _OK_button = tk.Button(master, text="OK", command=master.quit)
        _OK_button.pack(side=tk.TOP)

        # --- create canvas with scrollbar ---
        _canvas = tk.Canvas(master, width=1200, height=600)
        _canvas.pack(side=tk.LEFT)
        _scrollbar = tk.Scrollbar(master, command=_canvas.yview)
        _scrollbar.pack(side=tk.LEFT, fill='y')
        _canvas.configure(yscrollcommand=_scrollbar.set)
        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        _canvas.bind('<Configure>', lambda event: _canvas.configure(scrollregion=_canvas.bbox('all')))
        # --- put frame in canvas ---
        _frame = tk.Frame(_canvas)
        _canvas.create_window((0, 0), window=_frame, anchor='nw')
        # --- add widgets in frame ---
        _line_count = 0
        _col_count = 0
        _widths = (5, 110, 60, 10, 5, 5)
        for line in lines:
            _col_count = 0
            line = list(line)
            if _line_count:
                line.insert(0, str(_line_count))
            else:
                line.insert(0, '#')
            for item in line:
                mytext = tk.StringVar(value=item)
                text_entry = tk.Entry(_frame, textvariable=mytext, state='readonly', width=_widths[_col_count])
                # text_entry.pack(side = LEFT)
                text_entry.grid(row=_line_count, column=_col_count,
                                sticky=sticky_gen(_col_count))
                _col_count += 1
            _line_count += 1

        def _quit(self):
            master.quit()
        master.bind('<Return>', _quit)
        master.bind('<Escape>', _quit)

        _canvas.bind("<Up>", lambda event: _canvas.yview_scroll(-1, "units"))
        _canvas.bind("<Down>", lambda event: _canvas.yview_scroll(1, "units"))
        _canvas.bind_all("<MouseWheel>", lambda event: _canvas.yview_scroll(-1*int(event.delta/50), "units"))
        _canvas.focus_set()
