from ifind.models.game_avatar import GameAvatar
from ifind.models.game_avatar import CategoryPage
import os
import sys
import inspect
import random
sys.path.append(os.getcwd())


class RMIYCGameAvatar(GameAvatar):

    def _get_handler(self, context, *args):
        """
        Instantiate and return appropriate page handler using instance page attribute.

        """
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj):
                if obj.__name__ == context:
                    return obj(context, *args)



class CategoryPage(CategoryPage):
    """
    Page handler implementation of Category Page

    """
    def _get_shared_messages(self):
        """
        Assumptions:
                user = ?
                current_game = None

        """
        messages = ["Fuck ...",
                    "Fuck2...",
                    "Fuck3..."]

        return messages

    def _get_anonymous_messages(self):
        """
        Assumptions:
                user = None
                current_game = None

        """
        messages = ["Fuck4...",
                    "Fuck5!",
                    "Fuck6..."]

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

