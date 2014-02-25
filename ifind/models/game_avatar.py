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
SKIP = 'Skip'
HANDLERS = (INDEX,
            CATEGORY,
            GAME,
            GAME_OVER,
            SEARCH,
            SKIP)


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

        # get shared messages
        messages = self._get_shared_messages()

        if self.logged_in:
            # get logged in user messages
            messages += self._get_authenticated_messages()
        else:
            # get anonymous user messages
            messages += self._get_anonymous_messages()

        if not messages:
            raise ValueError("***** A list was empty! ****")

        # pick one and return
        return random.choice(messages)

    def _get_shared_messages(self):
        """
        Abstract method for shared message logic.

        """
        pass

    def _get_anonymous_messages(self):
        """
        Abstract method for anonymous message logic.

        """
        pass

    def _get_authenticated_messages(self):
        """
        Abstract method for user message logic.

        """
        pass


class IndexPage(Handler):
    """
    Page handler implementation of Index Page

    """
    def _get_shared_messages(self):
        """
        Assumptions:
                user = ?
                current_game = None

        """
        messages = ["Fancy a game?",
                    "Play a game!",
                    "Welcome!"]

        return messages

    def _get_anonymous_messages(self):
        """
        Assumptions:
                user = None
                current_game = None

        """
        messages = ["Check out how to play!",
                    "Have you registered an account yet?",
                    "Welcome to Pagefetch!"]

        return messages

    def _get_authenticated_messages(self):
        """
        Assumptions:
                user = User
                current_game = None

        """
        # "Fancy a game?"
        # "You've played X games, why not try another?"
        # "You're so close to achieving X achievement!"
        # "You've not logged in for ages :("
        # "You're around these parts pretty often!"
        # "Checked out your profile lately?"
        # "You're currently ranked Xth. You can do better!"

        messages = []

        messages.append("Hi {}, welcome back!".format(self.user.username))

        return messages


class CategoryPage(Handler):
    """
    Page handler implementation of Category Page

    """
    def _get_shared_messages(self):
        """
        Assumptions:
                user = ?
                current_game = None

        """
        messages = ["Pick a category...",
                    "Choose a category...",
                    "Please pick a category..."]

        return messages

    def _get_anonymous_messages(self):
        """
        Assumptions:
                user = None
                current_game = None

        """
        messages = ["That first category looks good...",
                    "Log in to see your high scores!",
                    "Any category will do..."]

        return messages

    def _get_authenticated_messages(self):
        """
        Assumptions:
                user = User
                current_game = None

        """
        messages = []

        #######  Recommend lesser/low scored categories. #######

        from ifind.models.game_models import HighScore

        high_scores = HighScore.objects.filter(user=self.user).order_by('highest_score')

        if high_scores:

            category = high_scores[0].category
            score = high_scores[0].highest_score

            messages.append('Your {} score is awfully low...'.format(category))
            messages.append('Only got {1} points for {0}?'.format(category, score))
            messages.append('Scared of trying {0}, {1}?'.format(category, self.user))

        return messages


class GamePage(Handler):
    """
    Page handler implementation of a Game Page (when playing)

    """
    def _get_shared_messages(self):
        """
        Assumptions:
                user=?, current_game

        """
        messages = ["Good luck!",
                    "Search til you drop!",
                    "The searching begins..."]

        return messages

    def _get_anonymous_messages(self):
        """
        Assumptions:
                user = None
                current_game = Game

        """
        messages = ["Get achievements when logged in!"]

        return messages

    def _get_authenticated_messages(self):
        """
        Assumptions:
                user = User
                current_game = Game

        """
        messages = []

        #######  Chide for small amount of games played thus far #######

        messages.append("Good luck {}!".format(self.user.username))

        return messages


class Search(Handler):
    """
    Handler implementation of a Search query AJAX request.

    """
    def _get_shared_messages(self):
        """
        Assumptions:
                user = ?
                current_game = Game

        """
        messages = []
        query_score = self.current_game.last_query_score

        ###### If user obtained 0 points with their query ######
        if query_score == 0:
            messages.append('You scored 0 points... unlucky...')
            messages.append("Let's try for some points this time!")
            messages.append('You can click (Enter) to search')

        ###### If user obtained less than 500 points with their query ######
        if 0 < query_score < 500:
            messages.append('Good. But not great...')
            messages.append("{} isn't a BAD score... just a bit low.".format(query_score))
            messages.append('You can click (Ctrl + Enter) to take the points and move on to the next round')
        #"Hmm, that's fair."
        if 500 <= query_score <= 700:
            messages.append('{} points is good!'.format(query_score))
        ###### If user obtained more than 700 points with their query ######
        if query_score > 700:
            messages.append('{} points? Well done...'.format(query_score))
            messages.append('{} points is pretty good!'.format(query_score))
            messages.append('You can click (Ctrl + Enter) to take the points and move on to the next round')

        if not messages:
            print query_score

        return messages

    def _get_anonymous_messages(self):
        """
        Assumptions:
                user = None
                current_game = Game

        """
        messages = []

        return messages

    def _get_authenticated_messages(self):
        """
        Assumptions:
                user = User
                current_game = Game

        """
        messages = []

        return messages


class Skip(Handler):
    """
    Handler implementation of a Search query AJAX request.

    """
    def _get_shared_messages(self):
        """
        Assumptions:
                user = ?
                current_game = Game

        """
        messages = []
        messages.append("You can click (Enter) to search")
        messages.append("Now look at this page carefully and enter a query")
        return messages

    def _get_anonymous_messages(self):
        """
        Assumptions:
                user = None
                current_game = Game

        """
        messages = []

        return messages

    def _get_authenticated_messages(self):
        """
        Assumptions:
                user = User
                current_game = Game

        """
        messages = []

        return messages


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
