import os
import functools
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--public", default=True, action="store_false",
                    help="Include example question catalogue instead of real")
parser.add_argument("--all", default=False, action="store_true",
                    help="Include executable in zip")
args = parser.parse_args()


# First pack release in unencrypted zip
command = '7z a -tzip'
distPath = 'dist'
if args.all:
    archivename = 'fuxenpruefung.zip'
    files = [r'"C:\Users\Andreas Maier\Documents\Fuxenpruefung\dist\fuxenpruefung.exe"']
    prefix = 'questions/'
    preCmd = ''
    mvCmd = None
else:
    archivename = 'questions.zip'
    files = []
    prefix = ''
    preCmd = 'cd questions & '
    mvCmd = ('questions/' + archivename, archivename)
question_file = ""
question_file = prefix + 'fragensammlung_beispiel.txt'
files.append(question_file)
question_file = prefix + 'example_questions.txt'
files.append(question_file)
question_file = prefix + 'fragensammlung_beispiel.zip'
files.append(question_file)
if not args.public:
    question_file = prefix + 'fragensammlung.txt'
    files.append(question_file)
allfiles = functools.reduce(lambda a, b: a + ' ' + b, files)
os.system('del '+archivename)
os.system(preCmd + command + ' ' + archivename + ' ' + allfiles)
if mvCmd:
    os.rename(*mvCmd)

# then encrypt secret question file
print('Also recreate encrypted question file? (Y/[n]):')
if input() == 'Y':
    archivename = 'fragensammlung.zip'
    os.system('del questions\\'+archivename)
    print('Enter password to encrypt question file:')
    passwd = input()
    command = 'cd questions & 7z a -tzip -p'+passwd+' '+archivename+' fragensammlung.txt'
    # command = 'cd questions & 7z a -tzip -p'+passwd+' '+archivename+' fragensammlung.txt'
    os.system(command)
