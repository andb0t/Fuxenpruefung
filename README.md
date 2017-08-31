<img src="src/images/fox.png" width="20"><img src="src/images/fox.png" width="50"><img src="src/images/fox.png" width="100"><img src="src/images/fox.png" width="50"><img src="src/images/fox.png" width="20">


# Fuxenprüfungsgenerator

### A program for random questionnaires

This is a small program to create a random questionnaire from a list of questions. It is primarily written for easily compiling and correcting exams.

The selection of questions is randomized, and so is the order of appearance. The number of questions from different categories of difficulty can be set.

The program creates two formatted text documents, the solutions for the examiner and the questionnaire for the examinee.




## Usage:
The program requires a question file, structured like the example question files in `questions` directory contained in the project and explained under *Question file syntax* below. It can also read input from an encrypted ZIP file, such as the one delivered within the project (password: *password*). This is useful if you do not want to risk your students to get hold of the answers.




## Installation
*No installation necessary!* The distributed ZIP file `fuxenpruefung.zip` in the [releases](https://github.com/andb0t/Fuxenpruefung/releases) contains the compiled windows executable. It also contains a directory of example questions. Simply download, extract and click.




## Languages:
The program is available in those languages:
* German <img src="src/images/ger.png" height="12">
* English <img src="src/images/eng.png" height="12">
* Bavarian <img src="src/images/bay.png" height="12">




## Keybindings:
* `<Escape>`    close the current window
* `<Up>`        radio button up
* `<Down>`      radio button down
* `<Return>`    start, proceed with next window
* `m`           in main window: mute or unmute sound
* `l`           in main window: switch language




## Question file syntax
The program expects questions in the following format, each part separated by a hash (#) from the other:
```
[Difficulty] # [Question] # [Answer] # [Category] # [Empty lines for answer]
```
The difficulty/work intensity related with a question is set via H (high), M (medium), S (small), J (joke), P (permanent), A (archived). For example:
```
S # What is the name of this program? # Fuxenprüfung # IT # 1
```
would denote a small question asking for the name of the program, which is an IT related question and needs one line for the answer *Fuxenprüfung*.

For Multiple Choice questions use '\\\\' for every option, e.g.:
```
S # What is python?\\A snake\\A programming language# A # Example # 0
```
would result in a multiple choice question with two bullet points and no space after it, since they are meant to be ticked.




## For the geeks:
If you would like to test it, tweak it, build it yourself or contribute, this is for you!

### Contributing
Suggestions, tips, issues, feature requests or merge requests are always welcome!

Simply create your own branch and go for it! An early pull request with the `WIP:` label allows us to discuss the change before it is time to merge.

### Alternative execution
If you would like to execute it via the shell use this:
```shell
$ cd src
$ python fuxenpruefung.py
```

### Dependencies and compilation
All used packages are part of the standard python distribution, the others are available via channels like `anaconda`. Most notabily, it uses `winsound` for playing music, so this feature only exists on windows, yet. If you want to compile the project from source, use this:
```shell
pyinstaller src/fuxenpruefung.spec
```
