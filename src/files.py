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


BEER_IMG_PATH = resource_path('', r'images\beer.png')
BUCKET_IMG_PATH = resource_path('', r'images\bucket.png')
FLOOR_IMG_PATH = resource_path('', r'images\floor.jpg')
FOX_ICO_PATH = resource_path('', r'images\fox.ico')
GOLD_FOX_ICO_PATH = resource_path('', r'images\gold_fox.png')
FOX_IMG_PATH = resource_path('', r'images\fox.png')
GITHUB_IMG_PATH = resource_path('', r'images\github.png')
MAJOR_IMG_PATH = resource_path('', r'images\major.png')
STAR_IMG_PATH = resource_path('', r'images\star.png')
JAEGER_IMG_PATH = resource_path('', r'images\jaeger.png')

SONG_WAV_PATH = resource_path('', r'sounds\Ehr_unser_Zier.wav')
BLOP_WAV_PATH = resource_path('', r'sounds\Blop.wav')
SLURP_WAV_PATH = resource_path('', r'sounds\Slurp.wav')
HICCUP_WAV_PATH = resource_path('', r'sounds\Hiccup.wav')
BLAST_WAV_PATH = resource_path('', r'sounds\Blast.wav')

SNAKE_CONFIG_FILE = '.fuxensnake_settings.yml'
