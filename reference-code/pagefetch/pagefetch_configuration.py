__author__ = 'leif'

import os
import socket
from utils import game_log

DEPLOYED = False
machine_base_dir = {'rabi.dcs.gla.ac.uk': '/Users/leif/Code/pagefetch/',
                    'king.dcs.gla.ac.uk': '/Users/jpurvis/Code/pagefetch/',
                    'general.dcs.gla.ac.uk': '/Users/0805976d/Documents/pagefetch',
                    'web305.webfaction.com': '/home/leifos/webapps/django/pagefetch'}

machine = socket.gethostname()
if DEPLOYED == True:
    work_dir = machine_base_dir[machine]
    data_dir = os.path.join(machine_base_dir[machine],"pagefetch/db")
    database_file_name = os.path.join(data_dir,"pagefetch-game.db")
    template_dir = os.path.join(work_dir, 'templates')
    media_dir = os.path.join(work_dir, 'site_media')
else:
    work_dir = machine_base_dir[machine]
    data_dir = os.path.join(machine_base_dir[machine],"pagefetchdata")
    database_file_name = os.path.join(data_dir,"pagefetch-game.db")
    template_dir = os.path.join(work_dir, 'pagefetch/templates')
    media_dir = os.path.join(work_dir, 'pagefetch/site_media')

print "machine: " + machine
print "work_dir: " + work_dir
print "data_dir: " + data_dir
print "db_file: " + database_file_name
print "template_dir: " + template_dir
print "media_dir: " + media_dir

#gamelog_filename = os.path.join(data_dir,'pagefetch-game.log')
#print "Creating game log: " + gamelog_filename
#game_log.create_game_logger(gamelog_filename)
