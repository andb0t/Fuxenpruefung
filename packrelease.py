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
archivename = 'Fuxenpruefung.zip'
files = [r'"C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\dist\Fuxenpruefung.exe"']
question_file = ""
question_file = 'Fragensammlung_Beispiel.txt'
files.append(question_file)
question_file = 'Example_questions.txt'
files.append(question_file)
if not options.ispublic:
    question_file = 'Fragensammlung.txt'
    files.append(question_file)
allfiles = functools.reduce(lambda a, b: a + ' ' + b, files)
os.system('del '+archivename)
os.system(command+' '+archivename+' '+allfiles)

# then encrypt secret question file
archivename = 'Fragensammlung.zip'
os.system('del '+archivename)
print('Enter password to encrypt question file:')
passwd = input()
command = '7z a -tzip -p'+passwd+' '+archivename+' Fragensammlung.txt'
os.system(command)
