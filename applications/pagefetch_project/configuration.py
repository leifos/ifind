__author__ = 'leif'
import os



PROJ_PATH = os.getcwd()
print "Project Path: %s" % (PROJ_PATH)
GAME_DB = os.path.join(PROJ_PATH, 'game.db')
TEMP_PATH = os.path.join(PROJ_PATH, 'templates')
STATIC_PATH = os.path.join(PROJ_PATH, 'static/')


MEDIA_URL = '/data/'
MEDIA_ROOT = os.path.join(PROJ_PATH, 'data') # Absolute path to the media directory
MEDIA_PATH = ''
UPLOAD_DIR =  '%Y/%m/%d'
DATA_DIR = os.path.join(PROJ_PATH, 'data')

DEPLOY = False
DEBUG = True

APP_NAME = 'pagefetch'
