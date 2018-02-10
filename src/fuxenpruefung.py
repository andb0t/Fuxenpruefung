import sys

import argparse
import tkinter as tk

import data
import i18n
import gui
import files
import tasks
try:
    import sound_win as sound
except ImportError:
    import sound_linux as sound


def change_catagories(category, categoryUpdate):
    for key in categoryUpdate.keys():
        try:
            catIdx = list(map(lambda a: a[2], category)).index(key)
        except ValueError:
            continue
        category[catIdx][0] = categoryUpdate[key]
    return category


parser = argparse.ArgumentParser()
parser.add_argument('--headless', action="store_true", default=False)
args = parser.parse_args()

sound.start_sound()
taskVar = 0
zipPasswd = ''
questionFile = ''
categoryUpdate = {}

if (args.headless):
    print('Finish early, headless GUI testing not yet implemented!')
    sys.exit()

while True:
    categories = [[16, i18n.longNames[i18n.lang()][0], i18n.shortNames[i18n.lang()][0]],
                  [6, i18n.longNames[i18n.lang()][1], i18n.shortNames[i18n.lang()][1]],
                  [4, i18n.longNames[i18n.lang()][2], i18n.shortNames[i18n.lang()][2]],
                  [1000, i18n.longNames[i18n.lang()][3], i18n.shortNames[i18n.lang()][3]],
                  [5, i18n.longNames[i18n.lang()][4], i18n.shortNames[i18n.lang()][4]],
                  [0, i18n.longNames[i18n.lang()][5], i18n.shortNames[i18n.lang()][5]],
                  ]
    change_catagories(categories, categoryUpdate)
    category_numbers = map(lambda x: x[0], categories)
    mainroot = tk.Tk()
    if sys.platform == 'win32':
        mainroot.iconbitmap(files.FOX_ICO_PATH)
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

    print('Selected task:', i18n.dictInit[i18n.lang()][taskVar])

    if taskVar == 4:
        mainroot.destroy()
        tasks.play_snake()
        continue

    try:
        zipFile, zipPasswd, questionFile = data.open_data(questionFile, zipPasswd)
    except TypeError:
        zipFile, zipPasswd = '', ''
        continue
    finally:
        mainroot.destroy()

    qdicts, qdictsAll = data.read_data(questNumbers, questionFile, zipFile, zipPasswd)

    if taskVar == 0:
        tasks.new_exam(qdicts, questNumbers, categories)

    elif taskVar == 1:
        tasks.show_statistics(qdicts, qdictsAll, categories)

    elif taskVar == 2:
        tasks.show_questions(qdictsAll)

    elif taskVar == 3:
        tasks.interactive_quiz(qdicts, questNumbers)
