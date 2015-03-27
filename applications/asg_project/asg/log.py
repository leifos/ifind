__author__ = 'leif'
import os
import logging
import logging.config
import logging.handlers

my_experiment_log_dir = os.getcwd()

event_logger = logging.getLogger('event_log')
event_logger.setLevel(logging.INFO)
event_logger_handler = logging.FileHandler(os.path.join(my_experiment_log_dir, 'move.log'))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
event_logger_handler.setFormatter(formatter)
event_logger.addHandler(event_logger_handler)

def log_move_event(game):


    move_pos = 0
    gain_list = []
    round = game.current_round

    game_num = game.id

    for i in round:
        r = round[i]
        if r['opened'] == True:
            i = i + 1
        gain_list.append(r['gain'])


    


    event_logger.info(msg='MOVE')