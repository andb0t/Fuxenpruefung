import os
import sys

import tkinter as tk

import files
import gui
import i18n

foxIco = files.resource_path('', r'images\fox.ico')


def read_data(questNumbers, questionFile, zipFile, zipPasswd):
    zipPasswd_bytes = str.encode(zipPasswd)

    qdicts = {}
    for key in questNumbers.keys():
        qdicts[key] = {}
    qdictsAll = {}

    questCounter = 0
    questLines = []
    if questionFile.endswith('.zip'):
        base = os.path.basename(questionFile)
        with zipFile.open(os.path.splitext(base)[0]+'.txt', pwd=zipPasswd_bytes) as data:
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
            if sys.platform == 'win32':
                root.iconbitmap(foxIco)
            root.title(i18n.errorTitle[i18n.lang()])
            lines = []
            lines.append(i18n.errorText[i18n.lang()][errorIdx] + ' ' + line)
            gui.InfoWindow(root, lines)
            root.focus_force()
            root.mainloop()
            root.destroy()
            zipPasswd = ''
            questionFile = ''
            continue

        qdicts[difficulty][len(qdicts[difficulty])] = question, answer, category, vspace
        qdictsAll[questCounter] = question, answer, category, difficulty, vspace
        questCounter += 1

    return qdicts, qdictsAll
