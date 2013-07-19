__author__ = 'arazzouk'
import os

PROJ_PATH = os.getcwd()
GAME_DB = os.path.join(PROJ_PATH, 'rmiyc.db')
TEMP_PATH = os.path.join(PROJ_PATH, 'templates')
STATIC_PATH = os.path.join(PROJ_PATH, 'static/')

MEDIA_PATH = ''
MEDIA_URL = '/data/'
MEDIA_ROOT = 'data/'
UPLOAD_DIR =  '%Y/%m/%d'
DATA_DIR = os.path.join(PROJ_PATH, 'data')

DEPLOY = False
DEBUG = True

APP_NAME = 'rmiyc'