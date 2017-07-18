import os
import functools
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-p", "--public", dest="ispublic", default=True,
                  action="store_false",
                  help="Include example question catalogue instead of real")
(options, args) = parser.parse_args()


# First pack release in unencrypted zip
command = '7z a -tzip'
archivename = 'fuxenpruefung.zip'
files = [r'"C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\dist\fuxenpruefung.exe"']
question_file = ""
question_file = 'questions/fragensammlung_beispiel.txt'
files.append(question_file)
question_file = 'questions/example_questions.txt'
files.append(question_file)
question_file = 'questions/fragensammlung_beispiel.zip'
files.append(question_file)
if not options.ispublic:
    question_file = 'questions/fragensammlung.txt'
    files.append(question_file)
allfiles = functools.reduce(lambda a, b: a + ' ' + b, files)
os.system('del '+archivename)
os.system(command+' '+archivename+' '+allfiles)

# then encrypt secret question file
print('Also recreate encrypted question file? (Y/n):')
if input() == 'Y':
    archivename = 'fragensammlung.zip'
    os.system('del '+archivename)
    print('Enter password to encrypt question file:')
    passwd = input()
    command = 'cd questions & 7z a -tzip -p'+passwd+' '+archivename+' fragensammlung.txt'
    os.system(command)
