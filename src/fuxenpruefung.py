import os
import random
import subprocess
import sys
import zipfile
from time import sleep

import tkinter as tk
from tkinter import filedialog, simpledialog

import i18n
import gui


def resource_path(base_path, relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


fox_ico = resource_path('', r'images\fox.ico')
fox_png = resource_path('', r'images\fox.png')
language_button_png = resource_path('', 'images\language.png')
github_button_png = resource_path('', 'images\github.png')
png_list = [fox_png, language_button_png, github_button_png]


def switch_language(lang):
    if lang == 'ger':
        return 'eng'
    elif lang == 'eng':
        return 'bay'
    elif lang == 'bay':
        return 'ger'


task_var = 0
zip_passwd = ''
question_file = ''
lang = 'ger'
while True:
    categories = [
                  [16, i18n.lg_names[lang][0], i18n.short_names[lang][0]],
                  [6, i18n.lg_names[lang][1], i18n.short_names[lang][1]],
                  [4, i18n.lg_names[lang][2], i18n.short_names[lang][2]],
                  [1000, i18n.lg_names[lang][3], i18n.short_names[lang][3]],
                  [5, i18n.lg_names[lang][4], i18n.short_names[lang][4]],
                  [0, i18n.lg_names[lang][5], i18n.short_names[lang][5]],
                 ]
    mainroot = tk.Tk()
    mainroot.iconbitmap(fox_ico)
    mainroot.title('Fux!')
    mainapp = gui.InitWindow(mainroot, categories, lang, png_list, task_var)
    mainroot.focus_force()
    mainroot.mainloop()
    if mainapp.switch_lang.get():
        lang = switch_language(lang)
    if mainapp.reinit.get():
        mainroot.destroy()
        continue
    task_var = mainapp.radio_var.get()
    idx = 0
    quest_numbers = {}
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
            zip_passwd = simpledialog.askstring(i18n.password_text[lang][0],
                                                i18n.password_text[lang][1], show='*')
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

    if not question_file or password_error:
        error_idx = 0
        if not question_file:
            error_idx = 0
        elif password_error:
            error_idx = 1
        root = tk.Tk()
        root.iconbitmap(fox_ico)
        root.title(i18n.error_title[lang])
        lines = []
        lines.append(i18n.error_text[lang][error_idx])
        app = gui.InfoWindow(root, lines)
        root.focus_force()
        root.mainloop()
        root.destroy()
        zip_passwd = ''
        question_file = ''
        continue

    print('Selected task:', i18n.dict_init[lang][task_var])

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
        splitlist = [x for x in map(lambda a: a.strip(), splitlist)]
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

        with open(i18n.exam_file[lang][0], 'w', encoding='utf8') as myfile:
            print(i18n.exam_title[lang][0]+"\n", file=myfile)
            count = 0
            for default, lg_name, short_name in categories:
                for question, answer, vspace in ran_qdicts[short_name]:
                    count += 1
                    questionlines = question.split("\\\\")
                    print('{}.'.format(count), questionlines[0], file=myfile)
                    for item in questionlines[1:]:
                        print('\to '+item, file=myfile)
                    print('\n'*int(vspace), file=myfile)

        with open(i18n.exam_file[lang][1], 'w', encoding='utf8') as myfile:
            print(i18n.exam_title[lang][1]+"\n", file=myfile)
            count = 0
            for default, lg_name, short_name in categories:
                for question, answer, vspace in ran_qdicts[short_name]:
                    count += 1
                    print('{}.'.format(count), answer, file=myfile)

        sys_command = 'notepad '+i18n.exam_file[lang][1]
        subprocess.Popen(sys_command)
        sleep(0.1)
        sys_command = 'notepad '+i18n.exam_file[lang][0]
        subprocess.Popen(sys_command)

    elif task_var == 1:
        from collections import Counter
        tot_n_questions = len(qdicts_all)
        # create message
        lines = []
        lines.append(i18n.statistics_header[lang][0])
        lines.append(i18n.statistics_colheader[lang])
        for default, lg_name, short_name in categories:
            lines.append((lg_name+': ', str(len(qdicts[short_name])),
                         '{:.0f} %'.format(100*len(qdicts[short_name])/tot_n_questions)))

        lines.append(i18n.statistics_header[lang][1])
        lines.append(i18n.statistics_colheader[lang])
        count_dict = Counter([x[2] for x in qdicts_all.values()])
        keys = list(count_dict.keys())
        keys.sort()
        for key in keys:
            lines.append((key+': ', str(count_dict[key]),
                         '{:.0f} %'.format(100*count_dict[key]/tot_n_questions)))

        root = tk.Tk()
        root.iconbitmap(fox_ico)
        root.title('Fux!')
        app = gui.InfoWindow(root, lines)
        root.focus_force()
        root.mainloop()
        root.destroy()

    elif task_var == 2:

        header = i18n.allquestions_header[lang]
        lines = []
        lines.append(i18n.allquestions_colheader[lang])
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
        app = gui.TextWindow(root, header, lines)
        root.focus_force()
        root.mainloop()
        root.destroy()
