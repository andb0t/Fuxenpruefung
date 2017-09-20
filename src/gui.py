import sys
import webbrowser

import tkinter as tk

import i18n
import gui_utils
try:
    import sound_linux as sound
except ImportError:
    import sound_win as sound
import files

foxPng = files.resource_path('', r'images\fox.png')
github_button_png = files.resource_path('', 'images\github.png')


def callback_GitHub(event):
    webbrowser.open_new(r"https://github.com/andb0t/Fuxenpruefung")


def callback_AGV(event):
    webbrowser.open_new(r"http://agv-muenchen.de/")


def set_image(button, file, zoom, height):
    newImg = tk.PhotoImage(file=file)
    newImg = newImg.subsample(zoom, zoom)
    button.configure(image=newImg, height=height)
    button.image = newImg


def set_text(field, text):
    field.configure(text=text)


def augment(tkVar, incr=1):
    tkVar.set(tkVar.get() + incr)


class InitWindow:

    def __init__(self, master, categories, radioinit=0):

        gui_utils.center_window(master)

        master.protocol("WM_DELETE_WINDOW", sys.exit)

        self.inputDict = {}
        self.radio_var = tk.IntVar()
        self.radio_var.set(radioinit)

        _row_count = 0

        _head_label = tk.Label(master, text=i18n.appHeader[i18n.lang()], font=("Helvetica", 16))
        _head_label.grid(row=_row_count, columnspan=4)
        _row_count += 1

        _photo = tk.PhotoImage(file=foxPng)
        _photo = _photo.subsample(5, 5)
        _photo_label = tk.Label(master, image=_photo)
        _photo_label.photo = _photo
        _photo_label.grid(row=_row_count, columnspan=4)
        _row_count += 1

        _col_idx = 0
        _row_count += 2
        _cat_label = []
        for idx, default in enumerate(categories):
            longName = i18n.longNames[i18n.lang()][idx]
            shortName = i18n.shortNames[i18n.lang()][idx]
            if shortName == 'P' or shortName == 'A':
                _cat_label.append(None)
                continue
            _cat_label.append(tk.Label(master, text=longName))
            _cat_label[-1].grid(row=_row_count-2, column=_col_idx, columnspan=2)
            string_val = tk.StringVar()
            string_val.set(default)
            cat_entry = tk.Entry(master, textvariable=string_val, width=5)
            cat_entry.grid(row=_row_count-1, column=_col_idx, columnspan=2)
            self.inputDict[shortName] = string_val
            _col_idx = (_col_idx + 2) % 4
            if (_col_idx == 0):
                _row_count += 2

        _radioButton = []
        for idx, task in enumerate(i18n.dictInit[i18n.lang()]):
            _radioButton.append(tk.Radiobutton(master, text=task, variable=self.radio_var, value=idx))
            _radioButton[idx].grid(row=_row_count, column=0, columnspan=4)
            _row_count += 1

        _start_button = tk.Button(master, text=i18n.startButtonText[i18n.lang()][0], fg="green", font="bold",
                                  command=master.quit)
        _start_button.grid(row=_row_count, column=0, columnspan=2)
        _quit_button = tk.Button(master, text=i18n.startButtonText[i18n.lang()][1], fg="red", font="bold",
                                 command=sys.exit)
        _quit_button.grid(row=_row_count, column=2, columnspan=2)
        _row_count += 1

        def set_switch_language():
            i18n.switch_language()
            set_image(_lang_button, i18n.lang_button_image(), 1, 20)
            set_text(_head_label, i18n.appHeader[i18n.lang()])
            for idx, rad in enumerate(_radioButton):
                set_text(rad, i18n.dictInit[i18n.lang()][idx])
            for idx, cat in enumerate(_cat_label):
                if cat is None:
                    continue
                set_text(cat, i18n.longNames[i18n.lang()][idx])
            set_text(_start_button, i18n.startButtonText[i18n.lang()][0])
            set_text(_quit_button, i18n.startButtonText[i18n.lang()][1])
            set_text(_link_label, i18n.linkLabelText[i18n.lang()])

        _lang_button = tk.Button(master, command=gui_utils.combine_funcs(set_switch_language))
        set_image(_lang_button, i18n.lang_button_image(), 1, 20)
        _lang_button.grid(row=_row_count, column=0)

        _github_button = tk.Button(master)
        set_image(_github_button, github_button_png, 5, 20)
        _github_button.bind("<Button-1>", callback_GitHub)
        _github_button.grid(row=_row_count, column=3)

        def set_toggle_sound():
            sound.toggle_sound()
            set_image(_sound_button, sound.sound_button_image(), 4, 20)

        _sound_button = tk.Button(master, command=gui_utils.combine_funcs(set_toggle_sound))
        set_image(_sound_button, sound.sound_button_image(), 4, 20)
        _sound_button.grid(row=_row_count, column=1)

        _link_label = tk.Label(master, text=i18n.linkLabelText[i18n.lang()], fg="blue", cursor="hand2")
        _link_label.grid(row=_row_count, column=2)
        _link_label.bind("<Button-1>", callback_AGV)

        thisradio = self.radio_var

        def _toggleup(self):
            old = thisradio.get()
            new = max(old - 1, 0)
            thisradio.set(new)

        def _toggledown(self):
            old = thisradio.get()
            new = min(old + 1, len(i18n.dictInit[i18n.lang()])-1)
            thisradio.set(new)

        def _quit(self):
            master.quit()

        def _mute(self):
            set_toggle_sound()

        def _lang(self):
            set_switch_language()

        master.bind('<Escape>', sys.exit)
        master.bind('<Up>', _toggleup)
        master.bind('<Down>',  _toggledown)
        master.bind('<Return>', _quit)
        master.bind('m', _mute)
        master.bind('l', _lang)


class InfoWindow:

    def __init__(self, master, lines):

        gui_utils.center_window(master)

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

        gui_utils.center_window(master)

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


class YesNoWindow:

    def __init__(self, master, lines):

        self.OKvalue = tk.IntVar()
        self.OKvalue.set(0)
        thisOKvalue = self.OKvalue

        gui_utils.center_window(master)
        master.protocol("WM_DELETE_WINDOW", master.quit)

        _row_count = 0
        for line in lines:
            one_msg = tk.Message(master, text=line, width=400)
            one_msg.grid(row=_row_count, column=0, columnspan=2)
            _row_count += 1

        def _quit():
            thisOKvalue.set(0)
            master.quit()

        def _go():
            thisOKvalue.set(1)
            master.quit()

        _OK_button = tk.Button(master, text=i18n.yesNo[i18n.lang()][0], command=_go, width=25)
        _OK_button.grid(row=_row_count, column=0)

        _cancel_button = tk.Button(master, text=i18n.yesNo[i18n.lang()][1], command=_quit, width=25)
        _cancel_button.grid(row=_row_count, column=1)

        def _quit_bind(self):
            _quit()

        def _go_bind(self):
            _go()

        master.bind('<Return>', _go_bind)
        master.bind('<Escape>', _quit_bind)


class QuizWindow:

    def __init__(self, master, questionList):

        self.quit = tk.IntVar()
        self.quit.set(0)
        thisQuit = self.quit

        self.success = tk.IntVar()
        self.success.set(0)
        thisSuccess = self.success

        self.failure = tk.IntVar()
        self.failure.set(0)
        thisFailure = self.failure

        self.skip = tk.IntVar()
        self.skip.set(0)
        thisSkip = self.skip

        self.currentQuestion = tk.IntVar()
        self.currentQuestion.set(0)
        thisCurrentQuestion = self.currentQuestion

        gui_utils.center_window(master)

        self.one_msg = []
        self._row_count = 0

        def _success():
            augment(thisSuccess)
            _new_question()

        def _failure():
            augment(thisFailure)
            _new_question()

        def _skip():
            augment(thisSkip)
            _new_question()

        def _quit():
            augment(thisQuit)
            master.quit()

        self._success_button = tk.Button(master, text=i18n.quizButton[i18n.lang()][0] + ' [k]',
                                         command=_success, width=15, font="bold")
        self._failure_button = tk.Button(master, text=i18n.quizButton[i18n.lang()][1] + ' [d]',
                                         command=_failure, width=15, font="bold")
        self._skip_button = tk.Button(master, text=i18n.quizButton[i18n.lang()][2] + ' [s]',
                                      command=_skip, width=15, font="bold")
        self._quit_button = tk.Button(master, text=i18n.quizButton[i18n.lang()][3] + ' [esc]',
                                      command=_quit, width=15, fg="red", font="bold")

        def print_question(one_msg):
            self._row_count = 0
            splitlist = questionList[self.currentQuestion.get()].split('\\\\')
            for idx, item in enumerate(splitlist):
                if idx > 0:
                    item = str(idx) + '. ' + item
                self.one_msg.append(tk.Message(master, text=item, width=575))
                self.one_msg[idx].grid(row=self._row_count, column=0, columnspan=4)
                self._row_count += 1
            self._failure_button.grid(row=self._row_count, column=1)
            self._success_button.grid(row=self._row_count, column=0)
            self._skip_button.grid(row=self._row_count, column=2)
            self._quit_button.grid(row=self._row_count, column=3)

        def remove_question(one_msg):
            while one_msg:
                msg = one_msg.pop()
                msg.grid_forget()

        print_question(self.one_msg)

        def _new_question():
            augment(thisCurrentQuestion)
            remove_question(self.one_msg)
            try:
                print_question(self.one_msg)
            except IndexError:
                master.quit()

        self._failure_button.grid(row=self._row_count, column=1)
        self._success_button.grid(row=self._row_count, column=0)
        self._skip_button.grid(row=self._row_count, column=2)
        self._quit_button.grid(row=self._row_count, column=3)

        def _success_bind(self):
            _success()

        def _failure_bind(self):
            _failure()

        def _skip_bind(self):
            _skip()

        def _quit_bind(self):
            _quit()

        master.protocol("WM_DELETE_WINDOW", _quit)
        master.bind('k', _success_bind)
        master.bind('d', _failure_bind)
        master.bind('s', _skip_bind)
        master.bind('<Escape>', _quit_bind)


class ResultWindow:

    def __init__(self, master, answers):
        gui_utils.center_window(master)
        master.protocol("WM_DELETE_WINDOW", master.quit)

        _row_count = 0
        _col_count = 0
        _widths = (200, 50, 50)
        _stickys = (tk.W, None, None)
        for line in answers:
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
