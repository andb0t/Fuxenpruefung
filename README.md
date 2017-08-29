Fuxenpruefungsgenerator

Description:
This is a small program to create a random questionnaire
from a list of questions. The selection of questions is
randomized, also the order of appearance. The number of
questions from different categories of difficulty can be
set.

The program creates two formatted text documents,
the solutions for the examiner and the questionnaire for
the examinee.


Cases of use:
This program is primarily written for easily compiling
and correcting exams.


Usage:
The program requires a question file, structured like the
example question files contained in the project. It can
also read input from an encrypted ZIP file, such as the
one delivered within the project (password: 'password').


Keybindings:
<Escape>    close the current window
<Up>        radio button up
<Down>      radio button down
<Return>    start, proceed with next window
m           in main window: mute or unmute sound


Languages:
The program is available in English, German and Bavarian.


Compilation for windows:
pyinstaller src/fuxenpruefung.spec
or
pyinstaller -w -F -i src/images/fox.ico src/fuxenpruefung.py
