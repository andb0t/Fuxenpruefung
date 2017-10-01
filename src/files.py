import sys
import os


def resource_path(basePath, relativePath):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(".")
    finalPath = os.path.join(basePath, relativePath)
    if sys.platform != 'win32':
        finalPath = finalPath.replace('\\', '/')
    return finalPath


beerImgPath = resource_path('', r'images\beer.png')
bucketImgPath = resource_path('', r'images\bucket.png')
floorImgPath = resource_path('', r'images\floor.jpg')
foxIco = resource_path('', r'images\fox.ico')
foxPng = resource_path('', r'images\fox.png')
github_button_png = resource_path('', 'images\github.png')
majorImgPath = resource_path('', r'images\major.png')
starImgPath = resource_path('', r'images\star.png')

songWav = resource_path('', r'sounds\Ehr_unser_Zier.wav')
blopWav = resource_path('', r'sounds\Blop.wav')
slurpWav = resource_path('', r'sounds\Slurp.wav')
hiccupWav = resource_path('', r'sounds\Hiccup.wav')
