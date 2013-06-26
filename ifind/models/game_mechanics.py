__author__ = 'leif'

from game_models import CurrentGame, Page, Category
from random import randint
from game_model_functions import get_page_list, set_page_list
from ifind.utils.rotation_ordering import RotationOrdering


MAX_SCORE = 1000
MAX_QUERIES = 20
MAX_PAGES = 2
MAX_QUERIES_PER_PAGE = 5
GAME_LENGTH_IN_SECONDS = 0


class GameMechanic(object):

    def __init__(self, current_game=None):
        """
        can be initialized with a reference to a ifind.models.game_models.CurrentGame
        :param current_game: ifind.models.game_models.CurrentGame
        :return: GameMechanic object
        """

        self.game = current_game


    def create_game(self, user, cat, game_type=0):
        """ create a new game for the user given the category
        set the cu
        :param user: User object
        :param cat: models.Category object
        :param pages: records from model.Page given cat
        :return: None
        """

        self.game = CurrentGame()

        #set starting values for game

        # get the pages associated with the category (cat)
        pages = get_pages_to_use(cat, game_type)

        #set starting page order for game
        self.create_page_ordering(pages)
        # now set the first page to find in the game
        self.set_next_page(pages)
        # save to db
        self.update_game()


    def retrieve_game(self, user, game_id):
        """ find the game associated with this user, and return the
            record from ifind.models.game_models.CurrentGame
        :param user:
        :param game_id:
        :return: True, if game is found, else False, if not
        """

        self.game = None
        found = False
        # look up model for game_id

        # if found, set self.game to game record

        return found


    def is_game_over(self):
        """ checks if the game is over
        :param game:
        :return: True if the end game criteria have been met, else False
        """
        # example criteria for the game end
        if (self.game.no_rounds >= MAX_PAGES) or (self.game.no_of_queries_issued <= MAX_QUERIES):
            return False
        else:
            return True


    def _increment_queries_issued(self, query_successful=False):
        self.game.no_of_queries_issued += 1
        self.game.no_of_queries_issued_for_current_page += 1
        if query_successful:
            self.game.no_of_successful_queries_issued +=1


    def _increment_score(self, points=0):
        self.game.current_score += points

    def update_game(self):
        """ make updates to game then save to db
        :param game:
        :return: None
        """
        self.game.save()

    def get_pages_to_use(self, cat, game_type):
        """ select a bunch of pages given the category and the game type
        :param cat:
        :param game_type:
        :return:
        """
        pass

    def create_page_ordering(self, pages, game):
        """ given a list of pages, create the ordering of pages for the game
        :param pages:
        :return:
        """
        # use the RotationOrdering class to gen the ordering
        ro = RotationOrdering()
        page_list = ro.get_ordering(pages)
        # set the page_list to the the game
        self.set_page_list(page_list)


    def set_next_page(pages, game):
        # from game get the page_list
        page_list = get_page_list(game)

        # given the round, select the page_id from page_list

        # associate the page from the page model to game

        pass


    def take_points():
        pass

    def handle_query(self, query_terms):

        # score the query
        # update self.game values


        pass




    def score_query(self, search_engine, query, url_to_find):
        """sends query to the search engine, checks if the page is returned,
           assign score to page, based on the rank
        :param query_terms: string
        :param url_to_find: string
        :return: integer
        """
        results = _run_query(search_engine, query)
        rank = _check_result(results, url_to_find)
        score = _score_rank(rank)
        return score

    def _run_query(self, search_engine, query):
        """ constructs ifind.search.query, and issues it to the search_engine

        :param search_engine:
        :param query:
        :return: ifind.search.response
        """
        pass

    def _check_result(self, response, url_to_find):
        """ iterates through the response looking for what rank the url is at

        :param response: ifind.search.response
        :param url_to_find: url string
        :return: rank of the url if found, else 0
        """

        return randint(0,10)


    def _score_rank(self, rank):
        """
        calculates the score based on the rank of the page
        :param rank: integer
        :return: integer
        """
        score = 0
        if rank > 0:
            score = round(MAX_SCORE / rank, 0)

        return score






