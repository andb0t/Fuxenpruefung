import sys
import os
import random
import tkinter as tk
from tkinter import filedialog, simpledialog
import webbrowser
import subprocess
import zipfile
from time import sleep


base_path = ''
# base_path = r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\\'
fox_png = base_path+r'Images\fox.png'
fox_ico = base_path+r'Images\fox.ico'
language_button_png = base_path+'Images\language.png'
github_button_png = base_path+'Images\github.png'
question_file = ''


reinit = False
current_lang = 'ger'

categories = []
lg_names = {'ger': ['Kleine Frage', 'Mittlere Frage', 'Große Frage', 'Permanente Frage',
                    'Scherzfrage', 'Archiv'],
            'eng': ['Small question', 'Medium question', 'Hard question', 'Permanent question',
                    'Joke question', 'Archive']}
short_names = {'ger': ['S', 'M', 'H', 'P', 'J', 'A'],
               'eng': ['S', 'M', 'H', 'P', 'J', 'A']}
start_button_text = []
start_button_texts = {'ger': ['Start', 'Schließen'],
                      'eng': ['Go!', 'Close']}
link_label_text = ''
link_label_texts = {'ger': 'AGV Webseite öffnen',
                    'eng': 'Open AGV website'}
error_title = ''
error_titles = {'ger': 'Fehler!',
                'eng': 'Error!'}
error_text = []
error_texts = {'ger': ['Keine Fragensammlung ausgewaehlt! Nochmal!', 'Falsches Passwort! Nochmal!'],
               'eng': ['No question file selected. Retry!', 'Bad password. Retry!']}
dict_init = []
dict_inits = {'ger': ['Erstelle neue Fuxenprüfung', 'Zeige Fragenstatistik', 'Zeige alle Fragen'],
              'eng': ['Compile new exam', 'Show question statistics', 'Show all questions']}
exam_title = []
exam_titles = {'ger': ['Fuxenprüfung', 'Fuxenlösung'],
               'eng': ['Exam', 'Solution']}
statistics_header = []
statistics_headers = {'ger': ['Fragenpool nach Schwierigkeit', 'Fragenpool nach Thema'],
                      'eng': ['Question pool by difficulty', 'Question pool by topic']}
statistics_colheader = []
statistics_colheaders = {'ger': ['Kategorie', 'Anzahl', 'Anteil'],
                         'eng': ['Category', 'Number', 'Fraction']}
allquestions_header = ''
allquestions_headers = {'ger': 'Alle verfügbaren Fragen und Antworten',
                        'eng': 'All available questions and answers'}
allquestions_colheader = []
allquestions_colheaders = {'ger': ['Frage', 'Antwort', 'Kateg.', 'Schw.', 'Platz'],
                           'eng': ['Question', 'Answer', 'Categ.', 'Diff.', 'Space']}
app_header = ''
app_headers = {'ger': 'Fuxenprüfungsgenerator',
               'eng': 'Exam generator'}
password_text = []
password_texts = {'ger': ['Passwort', 'Datei ist verschlüsselt! Bitte Passwort eingeben:'],
                  'eng': ['Password', 'File is encryoted! Please enter password:']}
exam_file = []
exam_files = {'ger': ['Fuxenpruefung.txt', 'Fuxenloesung.txt'],
              'eng': ['Exam.txt', 'Solution.txt']}


def setLanguage(key='ger'):
    global current_lang
    current_lang = key
    global categories
    categories = [
                  [16, lg_names[key][0], short_names[key][0]],
                  [6, lg_names[key][1], short_names[key][1]],
                  [4, lg_names[key][2], short_names[key][2]],
                  [1000, lg_names[key][3], short_names[key][3]],
                  [5, lg_names[key][4], short_names[key][4]],
                  [0, lg_names[key][5], short_names[key][5]],
                 ]
    global start_button_text
    start_button_text = start_button_texts[key]
    global link_label_text
    link_label_text = link_label_texts[key]
    global error_title
    error_title = error_titles[key]
    global error_text
    error_text = error_texts[key]
    global dict_init
    dict_init = dict_inits[key]
    global exam_title
    exam_title = exam_titles[key]
    global statistics_header
    statistics_header = statistics_headers[key]
    global statistics_colheader
    statistics_colheader = statistics_colheaders[key]
    global allquestions_header
    allquestions_header = allquestions_headers[key]
    global allquestions_colheader
    allquestions_colheader = allquestions_colheaders[key]
    global app_header
    app_header = app_headers[key]
    global password_text
    password_text = password_texts[key]
    global exam_file
    exam_file = exam_files[key]


def switchLanguage():
    if current_lang == 'ger':
        setLanguage('eng')
    elif current_lang == 'eng':
        setLanguage('ger')
    global reinit
    reinit = True


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
language_button_png = resource_path(language_button_png)
github_button_png = resource_path(github_button_png)


def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func


def callback_GitHub(event):
    webbrowser.open_new(r"https://github.com/andb0t/Fuxenpruefung/releases")


def callback_AGV(event):
    webbrowser.open_new(r"http://agv-muenchen.de/")


class InitWindow:

    def __init__(self, master, radioinit=0):

        master.protocol("WM_DELETE_WINDOW", sys.exit)

        self.input_dict = {}
        self.radio_var = tk.IntVar()
        _row_count = 0

        _head_label = tk.Label(master, text=app_header, font=("Helvetica", 16))
        _head_label.grid(row=_row_count, columnspan=4)
        _row_count += 1

        _photo = tk.PhotoImage(file=fox_png)
        _photo = _photo.subsample(5, 5)
        _photo_label = tk.Label(master, image=_photo)
        _photo_label.photo = _photo
        _photo_label.grid(row=_row_count, columnspan=4)
        _row_count += 1

        _col_idx = 0
        _row_count += 2
        for default, lg_name, short_name in categories:
            if short_name == 'P' or short_name == 'A':
                continue
            cat_label = tk.Label(master, text=lg_name)
            cat_label.grid(row=_row_count-2, column=_col_idx+1)
            string_val = tk.StringVar()
            string_val.set(default)
            cat_entry = tk.Entry(master, textvariable=string_val, width=5)
            cat_entry.grid(row=_row_count-1, column=_col_idx+1)
            self.input_dict[short_name] = string_val
            _col_idx = (_col_idx + 1) % 2
            if (_col_idx == 0):
                _row_count += 2

        for idx, task in enumerate(dict_init):
            rad = tk.Radiobutton(master, text=task, variable=self.radio_var, value=idx)
            rad.grid(row=_row_count, columnspan=4)
            _row_count += 1
        self.radio_var.set(radioinit)

        _start_button = tk.Button(master, text=start_button_text[0], fg="green", font="bold", command=master.quit)
        _start_button.grid(row=_row_count, column=0, columnspan=2)
        _quit_button = tk.Button(master, text=start_button_text[1], fg="red", font="bold", command=sys.exit)
        _quit_button.grid(row=_row_count, column=2, columnspan=2)
        _row_count += 1

        _language_button = tk.Button(master, command=combine_funcs(switchLanguage, master.quit))
        _language_button_image = tk.PhotoImage(file=language_button_png)
        _language_button_image = _language_button_image.subsample(3, 3)
        _language_button.config(image=_language_button_image, width=30, height=20)
        _language_button._language_button_image = _language_button_image
        _language_button.grid(row=_row_count, column=0)

        _github_button = tk.Button(master)
        _github_button_image = tk.PhotoImage(file=github_button_png)
        _github_button_image = _github_button_image.subsample(7, 7)
        _github_button.config(image=_github_button_image, width=60, height=20)
        _github_button._github_button_image = _github_button_image
        _github_button.bind("<Button-1>", callback_GitHub)
        _github_button.grid(row=_row_count, column=3)

        _link_label = tk.Label(master, text=link_label_text, fg="blue", cursor="hand2")
        _link_label.grid(row=_row_count, column=1, columnspan=2)
        _link_label.bind("<Button-1>", callback_AGV)


class InfoWindow:

    def __init__(self, master, lines):

        master.protocol("WM_DELETE_WINDOW", master.quit)

        _row_count = 0
        _col_count = 0
        _widths = (200, 50, 50)
        _stickys = (tk.W, None, None)
        for line in lines:
            if isinstance(line, str):
                one_msg = tk.Message(master, text=line, width=200)
                one_msg.grid(row=_row_count, columnspan=3)
            elif isinstance(line, tuple):
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


def sticky_gen(count):
    if count > 0:
        return tk.W


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
        _canvas.bind('<Configure>', make_on_configure(_canvas))
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
                text_entry = tk.Entry(_frame, textvariable=mytext,
                                   state='readonly', width=_widths[_col_count])
                # text_entry.pack(side = LEFT)
                text_entry.grid(row=_line_count, column=_col_count,
                                sticky=sticky_gen(_col_count))
                _col_count += 1
            _line_count += 1


task_var = 0
zip_passwd = ''
while True:

    setLanguage(current_lang)
    useGUI = True
    quest_numbers = {}
    if useGUI:
        mainroot = tk.Tk()
        mainroot.iconbitmap(fox_ico)
        mainroot.title('Fux!')
        mainapp = InitWindow(mainroot, task_var)
        mainroot.mainloop()
        if reinit:
            reinit = False
            mainroot.destroy()
            continue
        task_var = mainapp.radio_var.get()
        idx = 0
        for default, lg_name, short_name in categories:
            try:
                quest_numbers[short_name] = int((mainapp.input_dict)[short_name].get())
            except KeyError:
                quest_numbers[short_name] = default
            categories[idx][0] = quest_numbers[short_name]
            idx += 1

        # ask for question file
        FILEOPENOPTIONS = dict(initialdir='.', defaultextension='.txt', filetypes=[('', '*.txt;*.zip')])
        if not question_file:
            question_file = filedialog.askopenfilename(parent=mainroot, **FILEOPENOPTIONS)

        password_error = False
        if question_file.endswith('.zip'):
            zf = zipfile.ZipFile(question_file)
            for zinfo in zf.infolist():
                is_encrypted = zinfo.flag_bits & 0x1
            if is_encrypted and zip_passwd == '':
                zip_passwd = simpledialog.askstring(password_text[0], password_text[1], show='*')
                try:
                    zip_passwd_bytes = str.encode(zip_passwd)
                except TypeError:
                    zip_passwd_bytes = b'1234'
                print(os.path.splitext(question_file)[0])
                base = os.path.basename(question_file)
                try:
                    with zf.open(os.path.splitext(base)[0]+'.txt', pwd=zip_passwd_bytes) as data:
                        pass
                except RuntimeError:
                    print('Bad password!')
                    password_error = True

        mainroot.destroy()

    else:
        question_file = base_path+'Fragensammlung.txt'
        task_var = 0
        for default, lg_name, short_name in categories:
            quest_numbers[short_name] = default

    if not question_file or password_error:
        error_idx = 0
        if not question_file:
            error_idx = 0
        elif password_error:
            error_idx = 1
        root = tk.Tk()
        root.iconbitmap(fox_ico)
        root.title(error_title)
        lines = []
        lines.append(error_text[error_idx])
        app = InfoWindow(root, lines)
        root.mainloop()
        root.destroy()
        zip_passwd = ''
        question_file = ''
        continue

    print('Selected task:', dict_init[task_var])

    # Read in data
    qdicts = {}
    for key in quest_numbers.keys():
        qdicts[key] = {}
    qdicts_all = {}

    quest_counter = 0
    question_lines = []
    if question_file.endswith('.zip'):
        base = os.path.basename(question_file)
        with zf.open(os.path.splitext(base)[0]+'.txt', pwd=zip_passwd_bytes) as data:
            for byte_line in data:
                line = byte_line.decode('utf8')
                question_lines.append(line)
    else:
        with open(question_file, 'r', encoding='utf8') as data:
            for line in data:
                question_lines.append(line)

    for line in question_lines:
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

        with open(exam_file[0], 'w', encoding='utf8') as myfile:
            print(exam_title[0]+"\n", file=myfile)
            count = 0
            for default, lg_name, short_name in categories:
                for question, answer, vspace in ran_qdicts[short_name]:
                    count += 1
                    questionlines = question.split("\\\\")
                    print('{}.'.format(count), questionlines[0], file=myfile)
                    for item in questionlines[1:]:
                        print('\to '+item, file=myfile)
                    print('\n'*int(vspace), file=myfile)

        with open(exam_file[1], 'w', encoding='utf8') as myfile:
            print(exam_title[1]+"\n", file=myfile)
            count = 0
            for default, lg_name, short_name in categories:
                for question, answer, vspace in ran_qdicts[short_name]:
                    count += 1
                    print('{}.'.format(count), answer, file=myfile)

        sys_command = 'notepad '+exam_file[1]
        subprocess.Popen(sys_command)
        sleep(0.1)
        sys_command = 'notepad '+exam_file[0]
        subprocess.Popen(sys_command)

    elif task_var == 1:
        from collections import Counter
        tot_n_questions = len(qdicts_all)
        # create message
        lines = []
        lines.append(statistics_header[0])
        lines.append(statistics_colheaders)
        for default, lg_name, short_name in categories:
            lines.append((lg_name+': ', str(len(qdicts[short_name])),
                         '{:.0f} %'.format(100*len(qdicts[short_name])/tot_n_questions)))

        lines.append(statistics_header[1])
        lines.append(statistics_colheaders)
        count_dict = Counter([x[2] for x in qdicts_all.values()])
        keys = list(count_dict.keys())
        keys.sort()
        for key in keys:
            lines.append((key+': ', str(count_dict[key]),
                         '{:.0f} %'.format(100*count_dict[key]/tot_n_questions)))

        root = tk.Tk()
        root.iconbitmap(fox_ico)
        root.title('Fux!')
        app = InfoWindow(root, lines)
        root.mainloop()
        root.destroy()

    elif task_var == 2:

        header = allquestions_header
        lines = []
        lines.append(allquestions_colheader)
        for key in qdicts_all:
            lines.append((qdicts_all[key][0],
                          qdicts_all[key][1],
                          qdicts_all[key][2],
                          qdicts_all[key][3],
                          qdicts_all[key][4],
                          ))

        root = tk.Tk()
        root.iconbitmap(fox_ico)
        root.title('Fux!')
        app = TextWindow(root, header, lines)
        root.mainloop()
        root.destroy()

    if not useGUI:
        break
