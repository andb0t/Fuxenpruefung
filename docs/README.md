<img src="../src/images/fox.png" width="19"><img src="../src/images/fox.png" width="50"><img src="../src/images/fox.png" width="100"><img src="../src/images/fox.png" width="50"><img src="../src/images/fox.png" width="20">


# Fuxenprüfungsgenerator

[![Build status](https://travis-ci.org/andb0t/Fuxenpruefung.svg?branch=master)](https://travis-ci.org/andb0t)


### A program for random questionnaires

This is a small program to create a random questionnaire from a list of questions. It is primarily written for easily compiling and correcting exams.

A quiz and a snake game are provided as well for leisure time entertainment.

The program is available in those languages. Clicking the flag icon in the main window switches the language.
* German <img src="../src/images/ger.png" height="12">
* English <img src="../src/images/eng.png" height="12">
* Bavarian <img src="../src/images/bay.png" height="12">


### Content
* [Download](#download)
* [The fox snake game](#the-fox-snake-game)
* [The questionnaire generator](#the-questionnaire-generator)




## Download
The [releases](https://github.com/andb0t/Fuxenpruefung/releases) page contains all necessary downloads.

*No installation necessary!* Simply download the ready-made windows executable [here](https://github.com/andb0t/Fuxenpruefung/releases) and click!

You will also find there a `.zip` file containing example questions to get you started with the questionnaire.




## The fox snake game
Earn points by catching foxes but do not collide with your own tail. Besides that, follow the in-game instructions.





## The questionnaire generator

The selection of questions is randomized, and so is the order of appearance. The number of questions from different categories of difficulty can be set. The program creates two formatted text documents, the solutions for the examiner and the questionnaire for the examinee.

The program requires a question file, structured like the example question files in `questions` directory contained in the project and explained under *Question file syntax* below. It can also read input from an encrypted ZIP file, such as the one delivered within the project (password: *password*). This is useful if you do not want to risk your students to get hold of the answers.



### Question file syntax
If you would like to add, remove or change questions, this is your section. The program expects questions in the following format, each part separated by a hash (#) from the other:
```
[Difficulty] # [Question] # [Answer] # [Category] # [Empty lines for answer]
```
The difficulty/work intensity related with a question is set via H (high), M (medium), S (small), J (joke), P (permanent), A (archived). For example:
```
# What is the name of this program? # Fuxenprüfung # IT # 1
```
would denote a small question asking for the name of the program, which is an IT related question and needs one free line for the student's answer *Fuxenprüfung*.

For Multiple Choice questions use '\\\\' for every option, e.g.:
```
# What is python?\\A snake\\A programming language# A # Example # 0
```
would result in a multiple choice question with two bullet points and no space after it, since they are meant to be ticked.


### Keybindings
* `<Escape>`    close the current window
* `<Up>`        radio button up
* `<Down>`      radio button down
* `<Return>`    start, proceed with next window
* `m`           in main window: mute or unmute sound
* `l`           in main window: switch language
