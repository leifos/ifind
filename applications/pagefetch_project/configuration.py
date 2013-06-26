__author__ = 'leif'
import os

PROJ_PATH = os.getcwd()
GAME_DB = os.path.join(PROJ_PATH,'game.db')
TEMP_PATH = os.path.join(PROJ_PATH,'templates')
STATIC_PATH = os.path.join(PROJ_PATH,'static')
MEDIA_PATH = os.path.join(PROJ_PATH,'media')
MEDIA_URL  = os.path.join(PROJ_PATH,'media/')
UPLOAD_DIR = os.path.join(os.getcwd(),'media')

DEPLOY = False
DEBUG = True

APP_NAME = 'pagefetch'