<img src="src/images/fox.png" width="19"><img src="src/images/fox.png" width="50"><img src="src/images/fox.png" width="100"><img src="src/images/fox.png" width="50"><img src="src/images/fox.png" width="20">


# Fuxenprüfungsgenerator

### A program for random questionnaires

This is a small program to create a random questionnaire from a list of questions. It is primarily written for easily compiling and correcting exams.

The selection of questions is randomized, and so is the order of appearance. The number of questions from different categories of difficulty can be set. The program creates two formatted text documents, the solutions for the examiner and the questionnaire for the examinee.

A quiz and a snake game are provided as well for leisure time entertainment.

### Content
* [Installation](#installation)
* [Languages](#languages)
* [The questionnaire generator](#the-questionnaire-generator)
* [The fox snake game](#the-fox-snake-game)
* [For the geeks](#for-the-geeks)
* [Contributing](#contributing)



## Installation
The [releases](https://github.com/andb0t/Fuxenpruefung/releases) page contains all necessary downloads. You will also find there a `.zip` file containing example questions to get you started with the questionnaire.

### Windows
*No installation necessary!* Simply download the compiled windows executable [here](https://github.com/andb0t/Fuxenpruefung/releases) and click!

### Mac

Install system dependencies with [Homebrew](https://brew.sh/):

```shell
brew tap Homebrew/bundle
brew bundle install
```

Install Python dependencies with [Pipenv](https://docs.pipenv.org/):

```shell
pipenv install
```

Not fully working yet! Known issues:
- [ ] PNG files are not displayed

If you'd like to help, you are more than welcome! See [the contribution section](#contributing) for instructions.

### Linux
See chapter [for the geeks](#for-the-geeks). I guess you and me belong there :)



## Languages
The program is available in those languages. Clicking the flag icon in the main window switches the language.
* German <img src="src/images/ger.png" height="12">
* English <img src="src/images/eng.png" height="12">
* Bavarian <img src="src/images/bay.png" height="12">


## The questionnaire generator
The program requires a question file, structured like the example question files in `questions` directory contained in the project and explained under *Question file syntax* below. It can also read input from an encrypted ZIP file, such as the one delivered within the project (password: *password*). This is useful if you do not want to risk your students to get hold of the answers.




### Keybindings
* `<Escape>`    close the current window
* `<Up>`        radio button up
* `<Down>`      radio button down
* `<Return>`    start, proceed with next window
* `m`           in main window: mute or unmute sound
* `l`           in main window: switch language




### Question file syntax
The program expects questions in the following format, each part separated by a hash (#) from the other:
```
[Difficulty] # [Question] # [Answer] # [Category] # [Empty lines for answer]
```
The difficulty/work intensity related with a question is set via H (high), M (medium), S (small), J (joke), P (permanent), A (archived). For example:
```
# What is the name of this program? # Fuxenprüfung # IT # 1
```
would denote a small question asking for the name of the program, which is an IT related question and needs one line for the answer *Fuxenprüfung*.

For Multiple Choice questions use '\\\\' for every option, e.g.:
```
# What is python?\\A snake\\A programming language# A # Example # 0
```
would result in a multiple choice question with two bullet points and no space after it, since they are meant to be ticked.



## The fox snake game
Earn points by catching foxes but do not collide with your own tail. Besides that, follow the in-game instructions.


## For the geeks
If you would like to test it, tweak it, build it yourself or contribute, this is for you! Fork the project, clone it and start playing!

### Alternative execution
If you would like to execute it via the shell use this:
```shell
cd src
python3 fuxenpruefung.py
```
For starting the snake game only, do:
```shell
cd src
python3 snake.py
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
# yaml package: download wheel, e.g. from http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyyaml
pip install PyYAML-3.12-cp35-cp35m-win_amd64.whl
```
Then compile executable:
```shell
pyinstaller src/fuxenpruefung.spec
```




## Contributing
Suggestions, tips, issues, feature requests or merge requests are always welcome!

Simply create your own branch and go for it! An early pull request with the `WIP:` label allows us to discuss the change before it is time to merge.

### Continuous Integration
[![Build status](https://travis-ci.org/andb0t/iprofiler.png?branch=master)](https://travis-ci.org/andb0t)

### Contributors
The program has been designed and developed by
* [Andreas Maier](https://github.com/andb0t)

The following lists contributors, in alphabetical order
* [Kim Albertson](https://github.com/ashlaban)
