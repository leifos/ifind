""" Avatar Message Service -- Taking in UserProfile, HighSchores, CurrentGame & CurrentPage"""

import sys
import random
import inspect
import pprint as pp

#################
# PAGE HANDLERS #
#################

INDEX = "IndexPage"
CATEGORY = 'CategoryPage'
GAME = 'GamePage'
GAME_OVER = 'GameOverPage'

HANDLERS = (INDEX, CATEGORY, GAME, GAME_OVER)

DEBUG = True


class PageHandler(object):
    """
    Abstract class representing a site page.
    Each instance encapsulates a page's potential responses & related logic.

    """

    def __init__(self, page, user_profile=None, high_scores=None, current_game=None):

        self.page = page
        self.user_profile = user_profile
        self.high_scores = high_scores
        self.current_game = current_game
        self.logged_in = True if user_profile else False

    def get_message(self):
        """
        Public API to be used by GameAvatar.

        """
        if DEBUG:
            print
            pp.pprint(vars(self))
            print

        if self.logged_in:
            return self._get_user_message()
        elif not self.logged_in:
            return self._get_anonymous_message()

    def _get_anonymous_message(self):
        """
        Abstract method for anonymous message logic.

        """
        pass

    def _get_user_message(self):
        """
        Abstract method for user message logic.

        """
        pass


class IndexPage(PageHandler):
    """
    Page handler implementation of Index Page

    """
    def _get_anonymous_message(self):

        # Assumptions: user_profile=None, high_scores=None, current_game=None

        # "Welcome to RetrieveMeIfYouCan!"
        # "Why don't you try a game?"
        # "Check out how to play!"

        messages = ["Why don't you try a game?",
                    "Check out how to play!",
                    "Have you registered an account yet?",
                    "Welcome to Retrieve Me if You Can!",
                    "Fancy a game?"]

        return random.choice(messages)

    def _get_user_message(self):

        # Assumptions: user_profile, high_scores, current_game=None

        # "Fancy a game?"
        # "You've played X games, why not try another?"
        # "You're so close to achieving X achievement!"
        # "You've not logged in for ages :("
        # "You're around these parts pretty often!"
        # "Checked out your profile lately?"
        # "You're currently ranked Xth. You can do better!"

        return "Would you like to log out?"


class CategoryPage(PageHandler):
    """
    Page handler implementation of Category Page

    """

    def _get_anonymous_message(self):

        # Assumptions: user_profile=None, high_scores=None, current_game=None

        # "If you log in/register you can see your high scores for every category!"
        # "Pick a category!"

        messages = ["Pick a category!",
                    "The research one looks good...",
                    "Log in to see your high scores for each category!",
                    "Choose a category!"]

        return random.choice(messages)

    def _get_user_message(self):

        # Assumptions: user_profile, high_scores, current_game=None

        # "Pick a category!"
        # "You've not played any games in X category!"
        # "You've played A LOT of games in X category!"
        # "Been ages since you played!"

        return "Pick a category"


class GamePage(PageHandler):
    """
    Page handler implementation of a Game Page (when playing)

    """

    def _get_anonymous_message(self):

        # Assumptions: user_profile, high_scores, current_game

        if self.user_profile.no_games_played == 0:
            return "You can't get achievements without logging in :("




class GameAvatar (object):

    def __init__(self, page=None, user_profile=None, high_scores=None, current_game=None):

        self.page = page
        self.user_profile = user_profile
        self.high_scores = high_scores
        self.current_game = current_game

        if page:
            self._handler = self._get_handler(page, user_profile, high_scores, current_game)

    def send(self):
        """
        Send message to javascript avatar.
        (For now returns message to caller)

        Usage:
            avatar = GameAvatar(arg1, arg2, etc)
            avatar.send()

        """
        return self._handler.get_message()

    def update(self, page=None, user_profile=None, high_scores=None, current_game=None):
        """
        Update critical GameAvatar attributes, arguments are flexibly optional.

        Usage:
            avatar = GameAvatar(arg1)
            avatar.send()
            avatar.update(arg2)
            avatar.send()

        """
        if page is not None:
            self.page = page

        if user_profile is not None:
            self.user_profile = user_profile

        if high_scores is not None:
            self.high_scores = high_scores

        if current_game is not None:
            self.current_game = current_game

        self._handler = self._get_handler(self.page, self.user_profile, self.high_scores, self.current_game)

    def _get_handler(self, page, *args):
        """
        Instantiate and return appropriate page handler using instance page attribute.

        """
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj):
                if obj.__name__ == page:
                    return obj(page, *args)