import os, functools
command='7z a -tzip'
archivename='Fuxenpruefung.zip'
files=['fox.png', 'fox.ico', 'Fragensammlung.txt', r'"C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\dist\Fuxenpruefung.exe"']
allfiles=functools.reduce(lambda a,b:a+' '+b,files)
os.system(command+' '+archivename+' '+allfiles)
