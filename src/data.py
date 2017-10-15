import os
import sys
import zipfile

import tkinter as tk
from tkinter import filedialog, simpledialog

import files
import gui
import i18n


def open_data(questionFile, zipPasswd):
    fileOpenOptions = dict(initialdir='.', defaultextension='.txt', filetypes=[('', '*.txt;*.zip')])
    if not questionFile:
        questionFile = filedialog.askopenfilename(**fileOpenOptions)

    passwordError = False
    if questionFile != () and questionFile.endswith('.zip'):
        zipFile = zipfile.ZipFile(questionFile)
        for zinfo in zipFile.infolist():
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
                with zipFile.open(os.path.splitext(base)[0]+'.txt', pwd=zipPasswd_bytes):
                    pass
            except RuntimeError:
                print('Bad password!')
                passwordError = True
    else:
        zipFile = ''

    if passwordError:
        errorIdx = 1
        root = tk.Tk()
        if sys.platform == 'win32':
            root.iconbitmap(files.FOX_ICO_PATH)
        root.title(i18n.errorTitle[i18n.lang()])
        lines = []
        lines.append(i18n.errorText[i18n.lang()][errorIdx])
        gui.InfoWindow(root, lines)
        root.focus_force()
        root.mainloop()
        root.destroy()
        zipPasswd = ''
        questionFile = ''
        return

    if not questionFile:
        return

    return zipFile, zipPasswd, questionFile


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
                root.iconbitmap(files.FOX_ICO_PATH)
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
