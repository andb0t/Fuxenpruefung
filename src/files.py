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
