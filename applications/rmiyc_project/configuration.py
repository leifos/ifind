__author__ = 'arazzouk'
import os

PROJ_PATH = os.getcwd()
GAME_DB = os.path.join(PROJ_PATH, 'rmiyc.db')
TEMP_PATH = os.path.join(PROJ_PATH, 'templates')
STATIC_PATH = os.path.join(PROJ_PATH, 'static/')

MEDIA_PATH = ''
MEDIA_URL = ''
MEDIA_ROOT = 'imgs/'
UPLOAD_DIR = os.path.join(os.getcwd(), 'imgs/')
DATA_DIR = os.path.join(PROJ_PATH, 'data')

DEPLOY = False
DEBUG = True

APP_NAME = 'rmiyc'