<img src="src/images/fox.png" width="19"><img src="src/images/fox.png" width="50"><img src="src/images/fox.png" width="100"><img src="src/images/fox.png" width="50"><img src="src/images/fox.png" width="20">


# Fuxenprüfungsgenerator

[![Build status](https://travis-ci.org/andb0t/Fuxenpruefung.svg?branch=master)](https://travis-ci.org/andb0t)


### A program for random questionnaires

This is a small program to create a random questionnaire from a list of questions. It is primarily written for easily compiling and correcting exams.

A quiz and a snake game are provided as well for leisure time entertainment.

For more information on the usage of the program, please consult the public [webpage](https://andb0t.github.io/Fuxenpruefung).


### Content
* [Installation](#installation)
  * [Dependencies](#dependencies)
  * [Windows](#windows)
  * [Mac](#mac)
  * [Linux](#linux)
* [Development](#development)
  * [Contributing](#contributing)
  * [Contributors](#contributors)



## Installation
The [releases](https://github.com/andb0t/Fuxenpruefung/releases) page contains all necessary downloads. You will also find there a `.zip` file containing example questions to get you started with the questionnaire.


### Dependencies
Most of the packages used in this project are part of the standard python distribution, the others are available via package managers like `anaconda` or `pip`. The project uses python3. We recommend to use `pipenv` to manage the dependencies.


### Windows
To run the program from the shell:
```shell
pipenv install
cd src
python fuxenpruefung.py
```

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


### Mac

Install system dependencies with [Homebrew](https://brew.sh/):

```shell
brew tap Homebrew/bundle
brew bundle install
```

Install Python dependencies with [Pipenv](https://docs.pipenv.org/):

```shell
pipenv --three install
```

Not fully working yet! Known issues:
- [ ] PNG files are not displayed

If you'd like to help, you are more than welcome! See [the contribution section](#contributing) for instructions.

### Linux
Package manager packages are listed in `requirements.txt`. Some packages are not available via `pip` and have to be installed differently. The entire setup should look like this:
```shell
sudo apt-get install python3-tk python3-pil.imagetk python3-pyaudio
pip3 install -r requirements.txt
```





## Development
If you would like to test it, tweak it, build it yourself or contribute, this is for you! Fork the project, clone it and start playing!

```shell
cd src
python3 fuxenpruefung.py
```
For starting the snake game only, do:
```shell
cd src
python3 snake.py
```



### Contributing
Suggestions, tips, issues, feature requests or merge requests are always welcome!

Simply create your own branch and go for it! An early pull request with the `WIP:` label allows us to discuss the change before it is time to merge.




### Contributors
The program has been designed and developed by:
* [Andreas Maier](https://github.com/andb0t)

The following lists contributors in alphabetical order:
* [Kim Albertson](https://github.com/ashlaban)
