<img src="src/images/fox.png" width="19"><img src="src/images/fox.png" width="50"><img src="src/images/fox.png" width="100"><img src="src/images/fox.png" width="50"><img src="src/images/fox.png" width="20">


# Fuxenprüfungsgenerator

### A program for random questionnaires

This is a small program to create a random questionnaire from a list of questions. It is primarily written for easily compiling and correcting exams.

The selection of questions is randomized, and so is the order of appearance. The number of questions from different categories of difficulty can be set. The program creates two formatted text documents, the solutions for the examiner and the questionnaire for the examinee.

A quiz and a snake game are provided as well for leisure time entertainment.



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



## The fox snake game
Earn points by catching foxes but do not collide with your own tail.

* <img src="src/images/fox.png" height="20"> Appends a fox to your tail and spawns a new beer in case there isn't any left
* <img src="src/images/beer.png" height="20"> Raises the amount of points earned per fox, but increases the difficulty of nagivation. After consuming a beer there is a chance for another one to spawn.
* <img src="src/images/bucket.png" height="20"> The bucket resets the negative effects of beers but also reduces the beer count. Be careful, one more beer and you loose control!





## For the geeks:
If you would like to test it, tweak it, build it yourself or contribute, this is for you!

### Contributing
Suggestions, tips, issues, feature requests or merge requests are always welcome!

Simply create your own branch and go for it! An early pull request with the `WIP:` label allows us to discuss the change before it is time to merge.

### Alternative execution
If you would like to execute it via the shell use this:
```shell
$ cd src
$ python3 fuxenpruefung.py
```
For starting the snake game only, do:
```shell
$ cd src
$ python3 snake.py
```

### Dependencies and compilation
Most of the packages used in this project are part of the standard python distribution, the others are available via package managers like `anaconda` or `pip`. The project uses python3.

#### Linux
Package manager packages are listed in `requirements.txt`. Some packages are not available via `pip` and have to be installed differently. The entire setup should look like this:
```shell
sudo apt-get install python3-tk python3-pil.imagetk python3-pyaudio
pip3 install -r requirements.txt
```

#### Windows
If you want to compile the project from source first install the dependencies:
```shell
pip install requests==2.5.1  # pyinstaller 3.2.1 still has a bug with newer versions of requests
# yaml package: download correct wheel from http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyyaml
pip install PyYAML-3.12-cp35-cp35m-win_amd64.whl
```
Then compile executable:
```shell
iogndsagjsangsad
pyinstaller src/fuxenpruefung.spec
```


### Contributors
The program has been designed and developed by
* Andreas Maier, @andb0t
The following lists contributors, in alphabetical order
* Kim Albertson, @ashlaban
