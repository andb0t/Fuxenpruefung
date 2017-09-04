import os
import random
import subprocess
import zipfile
import functools
import operator
import time
import collections

import tkinter as tk
from tkinter import filedialog, simpledialog

import i18n
import gui
import files
import sound


def change_catagories(category, categoryUpdate):
    for key in categoryUpdate.keys():
        try:
            idx = list(map(lambda a: a[2], category)).index(key)
        except ValueError:
            continue
        category[idx][0] = categoryUpdate[key]
    return category


sound.start_sound()
taskVar = 0
zipPasswd = ''
questionFile = ''
categoryUpdate = {}
foxIco = files.resource_path('', r'images\fox.ico')


while True:

    lang_button_png = i18n.lang_button_image()
    sound_buttong_png = sound.sound_button_image()

    categories = [
                  [16, i18n.longNames[i18n.lang()][0], i18n.shortNames[i18n.lang()][0]],
                  [6, i18n.longNames[i18n.lang()][1], i18n.shortNames[i18n.lang()][1]],
                  [4, i18n.longNames[i18n.lang()][2], i18n.shortNames[i18n.lang()][2]],
                  [1000, i18n.longNames[i18n.lang()][3], i18n.shortNames[i18n.lang()][3]],
                  [5, i18n.longNames[i18n.lang()][4], i18n.shortNames[i18n.lang()][4]],
                  [0, i18n.longNames[i18n.lang()][5], i18n.shortNames[i18n.lang()][5]],
                 ]
    change_catagories(categories, categoryUpdate)
    category_numbers = map(lambda x: x[0], categories)
    mainroot = tk.Tk()
    mainroot.iconbitmap(foxIco)
    mainroot.title('Fux!')
    mainapp = gui.InitWindow(mainroot, category_numbers, taskVar)
    mainroot.focus_force()
    mainroot.mainloop()
    taskVar = mainapp.radio_var.get()
    idx = 0
    questNumbers = {}
    for idx, thisCat in enumerate(categories):
        default, longName, shortName = thisCat
        try:
            questNumbers[shortName] = categoryUpdate[shortName] = int((mainapp.inputDict)[shortName].get())
        except KeyError:
            questNumbers[shortName] = default
        categories[idx][0] = questNumbers[shortName]
        idx += 1

    # ask for question file
    FILEOPENOPTIONS = dict(initialdir='.', defaultextension='.txt', filetypes=[('', '*.txt;*.zip')])
    if not questionFile:
        questionFile = filedialog.askopenfilename(parent=mainroot, **FILEOPENOPTIONS)

    passwordError = False
    if questionFile.endswith('.zip'):
        zf = zipfile.ZipFile(questionFile)
        for zinfo in zf.infolist():
            isEncrypted = zinfo.flag_bits & 0x1
        if isEncrypted and zipPasswd == '':
            zipPasswd = simpledialog.askstring(i18n.passwordText[i18n.lang()][0],
                                               i18n.passwordText[i18n.lang()][1], show='*')
            try:
                zipPasswd_bytes = str.encode(zipPasswd)
            except TypeError:
                zipPasswd_bytes = b'1234'
            print(os.path.splitext(questionFile)[0])
            base = os.path.basename(questionFile)
            try:
                with zf.open(os.path.splitext(base)[0]+'.txt', pwd=zipPasswd_bytes) as data:
                    pass
            except RuntimeError:
                print('Bad password!')
                passwordError = True

    mainroot.destroy()

    if not questionFile or passwordError:
        errorIdx = 0
        if not questionFile:
            errorIdx = 0
        elif passwordError:
            errorIdx = 1
        root = tk.Tk()
        root.iconbitmap(foxIco)
        root.title(i18n.errorTitle[i18n.lang()])
        lines = []
        lines.append(i18n.errorText[i18n.lang()][errorIdx])
        app = gui.InfoWindow(root, lines)
        root.focus_force()
        root.mainloop()
        root.destroy()
        zipPasswd = ''
        questionFile = ''
        continue

    print('Selected task:', i18n.dictInit[i18n.lang()][taskVar])

    # Read in data
    qdicts = {}
    for key in questNumbers.keys():
        qdicts[key] = {}
    qdictsAll = {}

    questCounter = 0
    questLines = []
    if questionFile.endswith('.zip'):
        base = os.path.basename(questionFile)
        with zf.open(os.path.splitext(base)[0]+'.txt', pwd=zipPasswd_bytes) as data:
            for byteLine in data:
                line = byteLine.decode('utf8')
                questLines.append(line)
    else:
        with open(questionFile, 'r', encoding='utf8') as data:
            for line in data:
                questLines.append(line)

    for line in questLines:
        line = line.rstrip()
        if line.startswith('#') or not len(line):
            continue
        splitlist = []
        try:
            splitlist = line.split("#", 4)
        except ValueError:
            continue
        splitlist = [x for x in map(lambda a: a.strip(), splitlist)]
        try:
            difficulty, question, answer, category, vspace = splitlist
        except ValueError:
            errorIdx = 2
            root = tk.Tk()
            root.iconbitmap(foxIco)
            root.title(i18n.errorTitle[i18n.lang()])
            lines = []
            lines.append(i18n.errorText[i18n.lang()][errorIdx] + ' ' + line)
            app = gui.InfoWindow(root, lines)
            root.focus_force()
            root.mainloop()
            root.destroy()
            zipPasswd = ''
            questionFile = ''
            continue

        qdicts[difficulty][len(qdicts[difficulty])] = question, answer, category, vspace
        qdictsAll[questCounter] = question, answer, category, difficulty, vspace
        questCounter += 1

    def randomize_questions(exclude=''):
        ran_qdicts = {}
        for qdict_str in qdicts:
            if qdict_str in exclude:
                continue
            qdict = qdicts[qdict_str]
            keys = list(qdict.keys())
            random.shuffle(keys)
            ran_QnA = [(qdict[key][:2]+(qdict[key][3],)) for key in keys][:questNumbers[qdict_str]]
            ran_qdicts[qdict_str] = ran_QnA
        return ran_qdicts

    # process tasks below
    if taskVar == 0:
        ran_qdicts = randomize_questions()

        with open(i18n.examFile[i18n.lang()][0], 'w', encoding='utf8') as myfile:
            print(i18n.examTitle[i18n.lang()][0]+"\n", file=myfile)
            count = 0
            for default, longName, shortName in categories:
                for question, answer, vspace in ran_qdicts[shortName]:
                    count += 1
                    questionlines = question.split("\\\\")
                    print('{}.'.format(count), questionlines[0], file=myfile)
                    for item in questionlines[1:]:
                        print('\to '+item, file=myfile)
                    print('\n'*int(vspace), file=myfile)

        with open(i18n.examFile[i18n.lang()][1], 'w', encoding='utf8') as myfile:
            print(i18n.examTitle[i18n.lang()][1]+"\n", file=myfile)
            count = 0
            for default, longName, shortName in categories:
                for question, answer, vspace in ran_qdicts[shortName]:
                    count += 1
                    print('{}.'.format(count), answer, file=myfile)

        sys_command = 'notepad '+i18n.examFile[i18n.lang()][1]
        subprocess.Popen(sys_command)
        time.sleep(0.1)
        sys_command = 'notepad '+i18n.examFile[i18n.lang()][0]
        subprocess.Popen(sys_command)

    elif taskVar == 1:
        tot_n_questions = len(qdictsAll)
        # create message
        lines = []
        lines.append(i18n.statisticsHeader[i18n.lang()][0])
        lines.append(i18n.statisticsColHeader[i18n.lang()])
        for default, longName, shortName in categories:
            lines.append((longName+': ', str(len(qdicts[shortName])),
                         '{:.0f} %'.format(100*len(qdicts[shortName])/tot_n_questions)))

        lines.append(i18n.statisticsHeader[i18n.lang()][1])
        lines.append(i18n.statisticsColHeader[i18n.lang()])
        count_dict = collections.Counter([x[2] for x in qdictsAll.values()])
        keys = list(count_dict.keys())
        keys.sort()
        for key in keys:
            lines.append((key+': ', str(count_dict[key]), '{:.0f} %'.format(100*count_dict[key]/tot_n_questions)))

        root = tk.Tk()
        root.iconbitmap(foxIco)
        root.title('Fux!')
        app = gui.InfoWindow(root, lines)
        root.focus_force()
        root.mainloop()
        root.destroy()

    elif taskVar == 2:

        header = i18n.allquestionsHeader[i18n.lang()]
        lines = []
        lines.append(i18n.allquestionsColHeader[i18n.lang()])
        for key in qdictsAll:
            lines.append((qdictsAll[key][0],
                          qdictsAll[key][1],
                          qdictsAll[key][2],
                          qdictsAll[key][3],
                          qdictsAll[key][4],
                          ))
        root = tk.Tk()
        root.iconbitmap(foxIco)
        root.title('Fux!')
        app = gui.TextWindow(root, header, lines)
        root.focus_force()
        root.mainloop()
        root.destroy()

    elif taskVar == 3:

        ran_qdicts = randomize_questions(exclude=['J', 'P'])
        questionList = functools.reduce(operator.add, ran_qdicts.values())
        answersCount = [0, 0, 0]
        success = -1
        for idx, question in enumerate(questionList):
            root = tk.Tk()
            root.iconbitmap(foxIco)
            root.title(i18n.quizTitle[i18n.lang()])
            app = gui.QuizWindow(root, str(idx + 1) + '. ' + question[0])
            root.focus_force()
            root.mainloop()
            root.destroy()
            success = app.success.get()
            if success == -1:
                break
            else:
                answersCount[success] += 1

        if success == -1:
            continue

        # answersCount = {'success': 7, 'failure': 3, 'skip': 2}

        lines = []
        lines.append(i18n.successHeader[i18n.lang()][0])
        lines.append(i18n.statisticsColHeader[i18n.lang()])
        tot_n_questions = functools.reduce(operator.add, answersCount)
        successRate = answersCount[0]/(tot_n_questions - answersCount[2])
        successIndex = int(successRate * (len(i18n.successInterpretation[i18n.lang()]) - 1))
        successInterpretation = i18n.successInterpretation[i18n.lang()][successIndex]
        if successRate == 1:
            successInterpretation = i18n.successInterpretation[i18n.lang()][-1]

        keys = i18n.answerCorrect[i18n.lang()]
        for idx, key in enumerate(keys):
            lines.append((key+': ', str(answersCount[idx]), '{:.0f} %'.format(100*answersCount[idx]/tot_n_questions)))
        interpretationText = i18n.successHeader[i18n.lang()][1] + ': '
        interpretationText += str(int(100 * successRate)) + ' % '
        interpretationText += i18n.answerCorrect[i18n.lang()][0].lower() + '. '
        interpretationText += successInterpretation + '!'
        lines.append(interpretationText)

        root = tk.Tk()
        root.iconbitmap(foxIco)
        root.title('Fux!')
        app = gui.InfoWindow(root, lines)
        root.focus_force()
        root.mainloop()
        root.destroy()
