""" Avatar Message Service -- Taking in UserProfile, HighSchores, CurrentGame & CurrentPage"""

import sys
import random
import inspect
import pprint as pp

DEBUG = True

####################
# CONTEXT HANDLERS #
####################

# Pages

INDEX = "IndexPage"
CATEGORY = 'CategoryPage'
GAME = 'GamePage'
GAME_OVER = 'GameOverPage'

# Ajax

SEARCH = 'Search'

HANDLERS = (INDEX,
            CATEGORY,
            GAME,
            GAME_OVER,
            SEARCH)


class Handler(object):
    """
    Abstract class representing a site page.
    Each instance encapsulates a page's potential responses & related logic.

    """
    def __init__(self, context, user=None, current_game=None):

        self.context = context
        self.user = user
        self.current_game = current_game
        self.logged_in = True if user else False

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


class IndexPage(Handler):
    """
    Page handler implementation of Index Page

    """

    UNIVERSALS = ["Fancy a game?",
                  "Play a game!",
                  "Welcome :)"]

    def _get_anonymous_message(self):

        # Assumptions: user=None, current_game=None

        messages = ["Check out how to play!",
                    "Have you registered an account yet?",
                    "Welcome to Retrieve Me if You Can!"]

        messages += self.UNIVERSALS

        return random.choice(messages)

    def _get_user_message(self):

        # Assumptions: user, current_game=None

        # "Fancy a game?"
        # "You've played X games, why not try another?"
        # "You're so close to achieving X achievement!"
        # "You've not logged in for ages :("
        # "You're around these parts pretty often!"
        # "Checked out your profile lately?"
        # "You're currently ranked Xth. You can do better!"

        messages = []

        return "I am logged in and at index page"


class CategoryPage(Handler):
    """
    Page handler implementation of Category Page

    """

    UNIVERSALS = ["Pick a category...",
                  "Choose a category..."]

    def _get_anonymous_message(self):

        # user=None, current_game=None

        messages = ["That first category looks good...",
                    "Log in to see your high scores!",
                    "Any category will do..."]

        messages += self.UNIVERSALS

        return random.choice(messages)

    def _get_user_message(self):

        # user, current_game=None

        messages = []

        #######  Recommend lesser/low scored categories. ##########

        from ifind.models.game_models import HighScore

        high_scores = HighScore.objects.filter(user=self.user).order_by('highest_score')

        if high_scores:

            category = high_scores[0].category
            score = high_scores[0].highest_score

            messages.append('Your {} score is awfully low...'.format(category))
            messages.append('Only got {1} points for {0}?'.format(category, score))
            messages.append('Scared of trying {0}, {1}?'.format(category, self.user))

        ###########################################################

        messages += self.UNIVERSALS

        return random.choice(messages)

class GamePage(Handler):
    """
    Page handler implementation of a Game Page (when playing)

    """

    def _get_anonymous_message(self):

        # Assumptions: user=None, current_game

        return "Anonymous dude is starting.."

    def _get_user_message(self):

        # Assumptions: user, current_game

        return "Authorised legit dude is starting..."


class Search(Handler):
    """
    Handler implementation of a Search query AJAX request.

    """
    def _get_anonymous_message(self):

        # Assumptions: user=None, current_game

        return "Anonymous dude has searched!"

    def _get_user_message(self):

        # Assumptions: user, current_game

        if self.current_game.last_query_score == 0:
            # add to message list

        # if their score was above 900:
            # add to message list ("That was pretty good!")

            return "You're shite mate"


class GameAvatar (object):

    def __init__(self, context=None, user=None, current_game=None):

        self.context = context
        self.user = user
        self.current_game = current_game

        if context:
            self._handler = self._get_handler(context, user, current_game)

    def get(self):
        """
        Returns message within context of GameAvatar's arguments.

        Usage:
            avatar = GameAvatar(arg1, arg2, etc)
            avatar.send()

        """
        return self._handler.get_message()

    def update(self, context=None, user=None, current_game=None):
        """
        Update critical GameAvatar attributes, arguments are flexibly optional.

        Usage:
            avatar = GameAvatar(arg1)
            avatar.send()
            avatar.update(arg2)
            avatar.send()

        """
        if context is not None:
            self.page = context

        if user is not None:
            self.user = user

        if current_game is not None:
            self.current_game = current_game

        self._handler = self._get_handler(self.context, self.user, self.current_game)

    def _get_handler(self, context, *args):
        """
        Instantiate and return appropriate page handler using instance page attribute.

        """
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj):
                if obj.__name__ == context:
                    return obj(context, *args)