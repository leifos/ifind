__author__ = 'leif'
import logging

game_events = {0: "NOT_SPECIFIED",
               1: "START_GAME",
               3: "SHOW_PAGE",
               4: "ISSUED_QUERY",
               5: "PAGE_FOUND",
               6: "SKIP_PAGE",
               7: "BONUS",
               8: "PAGE_NOT_FOUND",
               9: "END_GAME" }

def create_game_logger(filename):
    game_logger = logging.getLogger('pagefetch_game_log')
    game_logger.setLevel(logging.INFO)
    game_logger_handler = logging.FileHandler(filename)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    game_logger_handler.setFormatter(formatter)
    game_logger.addHandler(game_logger_handler)


def log_game_event(request, event=0, query="", rank=None, score=None):
    """
    Assumes request holds cookie info for GameID, CatID, PageID
    Assumes rank and score are assumed to be integers when passed
    """

    game_logger = logging.getLogger('pagefetch_game_log')

    if event not in game_events:
        event = 0

    msg = "GID CatID PageID " + game_events[event]
    if query:
        msg += " " + query
    if rank:
        msg += " " + str(rank)
    if score:
        msg += " " + str(score)

    game_logger.info(msg)

