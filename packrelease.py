import os
import functools
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-p", "--public", dest="ispublic", default=True,
                  action="store_false",
                  help="Include example question catalogue instead of real")
(options, args) = parser.parse_args()

command = '7z a -tzip'
archivename = 'Fuxenpruefung.zip'
files = [r'"C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\dist\Fuxenpruefung.exe"']
question_file = ""
if options.ispublic:
    question_file = 'Fragensammlung_Beispiel.txt'
else:
    question_file = 'Fragensammlung.txt'
files.append(question_file)
allfiles = functools.reduce(lambda a, b: a + ' ' + b, files)

os.system('del '+archivename)
os.system(command+' '+archivename+' '+allfiles)
