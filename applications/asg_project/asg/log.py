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

def log_move_event(uid,game):

    gain_list = []
    round = game.current_round
    pos = 0
    for i in range(len(round)):
        r = round[i]
        if r['opened'] == True:
            pos = pos + 1
        gain_list.append(str(r['gain']))

    print gain_list

    gain_str = ' '.join(gain_list)

    msg = 'MOVE {0} {1} {2} {3}'.format(uid, game.id, pos, gain_str)
    event_logger.info(msg=msg)