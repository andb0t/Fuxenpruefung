import collections
import functools
import operator
import random
import subprocess
import sys
import time

import tkinter as tk

import files
import gui
import i18n
import snake


def randomize_questions(qdicts, questNumbers, exclude=''):
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


def new_exam(qdicts, questNumbers, categories):
    ran_qdicts = randomize_questions(qdicts, questNumbers)

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

    if sys.platform == 'win32':
        sys_command = 'notepad '+i18n.examFile[i18n.lang()][1]
        subprocess.Popen(sys_command)
        time.sleep(0.1)
        sys_command = 'notepad '+i18n.examFile[i18n.lang()][0]
        subprocess.Popen(sys_command)


def interactive_quiz(qdicts, questNumbers):
    ran_qdicts = randomize_questions(qdicts, questNumbers, exclude=['J', 'P'])
    questionList = functools.reduce(operator.add, ran_qdicts.values())
    questionList = map(lambda x: x[0], questionList)
    answersCount = [0, 0, 0]

    root = tk.Tk()
    if sys.platform == 'win32':
        root.iconbitmap(files.FOX_ICO_PATH)
    root.title(i18n.quizTitle[i18n.lang()])
    questionList = [str(idx + 1) + '. ' + question for idx, question in enumerate(questionList)]
    app = gui.QuizWindow(root, questionList)
    root.focus_force()
    root.mainloop()
    root.destroy()
    if app.quit.get():
        return
    success = app.success.get()
    failure = app.failure.get()
    skip = app.skip.get()
    if not (success + failure):
        return

    answersCount = [success, failure, skip]

    lines = []
    lines.append(i18n.quizHeader[i18n.lang()][0])
    lines.append(i18n.statisticsColHeader[i18n.lang()])
    tot_n_questions = functools.reduce(operator.add, answersCount)
    successRate = answersCount[0]/(tot_n_questions - answersCount[2])
    successIndex = int(successRate * (len(i18n.quizInterpretation[i18n.lang()]) - 1))
    quizInterpretation = i18n.quizInterpretation[i18n.lang()][successIndex]
    if successRate == 1:
        quizInterpretation = i18n.quizInterpretation[i18n.lang()][-1]

    keys = i18n.answerCorrect[i18n.lang()]
    for idx, key in enumerate(keys):
        lines.append((key+': ', str(answersCount[idx]), '{:.0f} %'.format(100*answersCount[idx]/tot_n_questions)))
    interpretationText = i18n.quizHeader[i18n.lang()][1] + ': '
    interpretationText += str(int(100 * successRate)) + ' % '
    interpretationText += i18n.quizCorrect[i18n.lang()] + '. '
    interpretationText += quizInterpretation + '!'
    lines.append(interpretationText)

    root = tk.Tk()
    if sys.platform == 'win32':
        root.iconbitmap(files.FOX_ICO_PATH)
    root.title('Fux!')
    app = gui.InfoWindow(root, lines)
    root.focus_force()
    root.mainloop()
    root.destroy()


def show_questions(qdictsAll):
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
    if sys.platform == 'win32':
        root.iconbitmap(files.FOX_ICO_PATH)
    root.title('Fux!')
    gui.TextWindow(root, header, lines)
    root.focus_force()
    root.mainloop()
    root.destroy()


def show_statistics(qdicts, qdictsAll, categories):
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
    if sys.platform == 'win32':
        root.iconbitmap(files.FOX_ICO_PATH)
    root.title('Fux!')
    gui.InfoWindow(root, lines)
    root.focus_force()
    root.mainloop()
    root.destroy()


def play_snake():
    root = tk.Tk()
    if sys.platform == 'win32':
        root.iconbitmap(files.FOX_ICO_PATH)
    root.title(i18n.snakeWelcome[i18n.lang()])
    snake.SnakeWindow(root)
    root.focus_force()
    root.mainloop()
    root.destroy()
