import sys
import os
import random
from tkinter import *
from tkinter import filedialog
import webbrowser
import subprocess


# user interface
dict_init = {}
dict_init[0] = 'Erstelle neue Fuxenprüfung'
dict_init[1] = 'Zeige Fragenstatistik'
dict_init[2] = 'Zeige alle Fragen'

base_path = ''
# base_path = r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\\'
fox_png = base_path+'fox.png'
fox_ico = base_path+'fox.ico'
answer_file = 'Fuxenloesung.txt'
test_file = 'Fuxenpruefung.txt'
question_file = ''


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


fox_png = resource_path(fox_png)
fox_ico = resource_path(fox_ico)


categories = [
              [16, 'Kleine Fragen', 'K'],
              [6, 'Mittlere Fragen', 'M'],
              [4, 'Große Fragen', 'G'],
              [1000, 'Permanente Fragen', 'P'],
              [5, 'Scherzfragen', 'S'],
              [0, 'Archiv', 'A'],
             ]


def callback(event):
    webbrowser.open_new(r"https://github.com/andb0t/Fuxenpruefung/releases")


class InitWindow:

    def __init__(self, master, radioinit=0):

        master.protocol("WM_DELETE_WINDOW", exit)

        self.input_dict = {}
        self.radio_var = IntVar()
        _row_count = 0

        _head_label = Label(master, text='Fuxenprüfungsgenerator', font=("Helvetica", 16))
        _head_label.grid(row=_row_count, columnspan=2)
        _row_count += 1

        _photo = PhotoImage(file=fox_png)
        _photo = _photo.subsample(5, 5)
        _photo_label = Label(master, image=_photo)
        _photo_label.photo = _photo
        _photo_label.grid(row=_row_count, columnspan=2)
        _row_count += 1

        _col_idx = 0
        _row_count += 2
        for default, lg_name, short_name in categories:
            if short_name == 'P' or short_name == 'A':
                continue
            cat_label = Label(master, text=lg_name)
            cat_label.grid(row=_row_count-2, column=_col_idx)
            string_val = StringVar()
            string_val.set(default)
            cat_entry = Entry(master, textvariable=string_val, width=5)
            cat_entry.grid(row=_row_count-1, column=_col_idx)
            self.input_dict[short_name] = string_val
            _col_idx = (_col_idx + 1) % 2
            if (_col_idx == 0):
                _row_count += 2

        for key in dict_init.keys():
            rad = Radiobutton(master, text=dict_init[key],
                              variable=self.radio_var, value=key)
            rad.grid(row=_row_count, columnspan=2)
            _row_count += 1
        self.radio_var.set(radioinit)

        _start_button = Button(master, text="Start", fg="green",
                               command=master.quit)
        _start_button.grid(row=_row_count, column=0)
        _quit_button = Button(master, text="Schließen", fg="red",
                              command=sys.exit)
        _quit_button.grid(row=_row_count, column=1)
        _row_count += 1

        _link_label = Label(master, text="Open on GitHub", fg="blue",
                            cursor="hand2")
        _link_label.grid(row=_row_count, column=0, columnspan=2)
        _link_label.bind("<Button-1>", callback)


class InfoWindow:

    def __init__(self, master, lines):

        master.protocol("WM_DELETE_WINDOW", master.quit)

        _row_count = 0
        _col_count = 0
        _widths = (200, 50, 50)
        _stickys = (W, None, None)
        for line in lines:
            if isinstance(line, str):
                one_msg = Message(master, text=line, width=200)
                one_msg.grid(row=_row_count, columnspan=3)
            elif isinstance(line, tuple):
                _col_count = 0
                for item in line:
                    multi_msg = Message(master, text=line[_col_count],
                                        width=_widths[_col_count])
                    multi_msg.grid(row=_row_count, column=_col_count,
                                   sticky=_stickys[_col_count])
                    _col_count += 1
            _row_count += 1

        _OK_button = Button(master, text="OK", command=master.quit)
        _OK_button.grid(row=_row_count, columnspan=3)


def sticky_gen(count):
    if count > 0:
        return W


def mystrip(a):
    return a.strip()


def make_on_configure(canvas):
    def on_configure(event):
        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        canvas.configure(scrollregion=canvas.bbox('all'))
    return on_configure


class TextWindow:

    def __init__(self, master, header, lines):

        master.protocol("WM_DELETE_WINDOW", master.quit)

        _head_label = Label(master, text=header)
        _head_label.pack(side=TOP)

        _OK_button = Button(master, text="OK", command=master.quit)
        _OK_button.pack(side=TOP)

        # --- create canvas with scrollbar ---
        _canvas = Canvas(master, width=1200, height=600)
        _canvas.pack(side=LEFT)
        _scrollbar = Scrollbar(master, command=_canvas.yview)
        _scrollbar.pack(side=LEFT, fill='y')
        _canvas.configure(yscrollcommand=_scrollbar.set)
        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        _canvas.bind('<Configure>', make_on_configure(_canvas))
        # --- put frame in canvas ---
        _frame = Frame(_canvas)
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
                mytext = StringVar(value=item)
                text_entry = Entry(_frame, textvariable=mytext,
                                   state='readonly', width=_widths[_col_count])
                # text_entry.pack(side = LEFT)
                text_entry.grid(row=_line_count, column=_col_count,
                                sticky=sticky_gen(_col_count))
                _col_count += 1
            _line_count += 1


task_var = 0
while True:

    useGUI = True
    quest_numbers = {}
    if useGUI:
        mainroot = Tk()
        mainroot.iconbitmap(fox_ico)
        mainroot.title('Fux!')

        FILEOPENOPTIONS = dict(initialdir='.', defaultextension='.txt',
                               filetypes=[('Text files', '*.txt')])
        if not question_file:
            question_file = filedialog.askopenfilename(parent=mainroot, **FILEOPENOPTIONS)

        mainapp = InitWindow(mainroot, task_var)
        mainroot.mainloop()
        task_var = mainapp.radio_var.get()
        idx = 0
        for default, lg_name, short_name in categories:
            try:
                quest_numbers[short_name] = int((mainapp.input_dict)[short_name].get())
            except KeyError:
                quest_numbers[short_name] = default
            categories[idx][0] = quest_numbers[short_name]
            idx += 1
        mainroot.destroy()
    else:
        question_file = base_path+'Fragensammlung.txt'
        task_var = 0
        for default, lg_name, short_name in categories:
            quest_numbers[short_name] = default

    print('Gewaehlte Aufgabe:', dict_init[task_var])
    if not question_file:
        root = Tk()
        root.iconbitmap(fox_ico)
        root.title('Fehler!')
        lines = []
        lines.append('Keine Fragensammlung ausgewaehlt! Nochmal!')
        app = InfoWindow(root, lines)
        root.mainloop()
        root.destroy()
        continue

    # Read in data
    qdicts = {}
    for key in quest_numbers.keys():
        qdicts[key] = {}
    qdicts_all = {}

    quest_counter = 0
    with open(question_file, 'r', encoding='utf8') as data:
        for line in data:
            line = line.rstrip()
            if line.startswith('#') or not len(line):
                continue
            splitlist = []
            try:
                splitlist = line.split("#", 4)
            except ValueError:
                continue
            splitlist = [x for x in map(mystrip, splitlist)]
            difficulty, question, answer, category, vspace = splitlist
            qdicts[difficulty][len(qdicts[difficulty])] = question, answer, category, vspace
            qdicts_all[quest_counter] = question, answer, category, difficulty, vspace
            quest_counter += 1

    if task_var == 0:
        ran_qdicts = {}
        for qdict_str in qdicts:
            qdict = qdicts[qdict_str]
            keys = list(qdict.keys())
            random.shuffle(keys)
            ran_QnA = [(qdict[key][:2]+(qdict[key][3],)) for key in keys][:quest_numbers[qdict_str]]
            ran_qdicts[qdict_str] = ran_QnA

        with open(test_file, 'w', encoding='utf8') as myfile:
            print("Fuxenprüfung\n", file=myfile)
            count = 0
            for default, lg_name, short_name in categories:
                for question, answer, vspace in ran_qdicts[short_name]:
                    count += 1
                    questionlines = question.split("\\\\")
                    print('{}.'.format(count), questionlines[0], file=myfile)
                    for item in questionlines[1:]:
                        print('\to '+item, file=myfile)
                    print('\n'*int(vspace), file=myfile)

        sys_command = 'notepad '+test_file
        # os.system(sys_command)
        subprocess.Popen(sys_command)

    elif task_var == 1:
        from collections import Counter
        tot_n_questions = len(qdicts_all)
        # create message
        lines = []
        lines.append('Fragenpool nach Schwierigkeit')
        lines.append(('Kategorie', 'Anzahl', 'Anteil'))
        for default, lg_name, short_name in categories:
            lines.append((lg_name+': ', str(len(qdicts[short_name])),
                         '{:.0f} %'.format(100*len(qdicts[short_name])/tot_n_questions)))

        lines.append('Fragenpool nach Thema')
        lines.append(('Kategorie', 'Anzahl', 'Anteil'))
        count_dict = Counter([x[2] for x in qdicts_all.values()])
        keys = list(count_dict.keys())
        keys.sort()
        for key in keys:
            lines.append((key+': ', str(count_dict[key]),
                         '{:.0f} %'.format(100*count_dict[key]/tot_n_questions)))

        root = Tk()
        root.iconbitmap(fox_ico)
        root.title('Fux!')
        app = InfoWindow(root, lines)
        root.mainloop()
        root.destroy()

    elif task_var == 2:

        header = 'Alle verfügbaren Fragen und Antworten'
        lines = []
        lines.append(('Frage', 'Antwort', 'Kateg.', 'Schw.', 'Platz'))
        for key in qdicts_all:
            lines.append((qdicts_all[key][0],
                          qdicts_all[key][1],
                          qdicts_all[key][2],
                          qdicts_all[key][3],
                          qdicts_all[key][4],
                          ))

        root = Tk()
        root.iconbitmap(fox_ico)
        root.title('Fux!')
        app = TextWindow(root, header, lines)
        root.mainloop()
        root.destroy()

    if not useGUI:
        break
