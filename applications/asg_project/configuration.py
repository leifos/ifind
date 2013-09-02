__author__ = 'leif'
import os

PROJ_PATH = os.getcwd()
GAME_DB = os.path.join(PROJ_PATH, 'asg.db')
TEMP_PATH = os.path.join(PROJ_PATH, 'templates')
STATIC_PATH = os.path.join(PROJ_PATH, 'static/')

MEDIA_PATH = ''
MEDIA_URL = '/data/'
MEDIA_ROOT = 'data/'
UPLOAD_DIR =  '%Y/%m/%d'
DATA_DIR = os.path.join(PROJ_PATH, 'data')

DEPLOY = True
DEBUG = False

APP_NAME = 'asg'