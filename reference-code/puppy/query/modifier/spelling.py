from puppy.lang import Languages
from puppy.model import Query
from puppy.query import ensure_query, QueryModifier


class SpellingCorrectingModifier(QueryModifier):
    """
    This modifies queries by replacing mispelt words with the first "correct" spelling found.

    Parameters:

    * order (int): modifier precedence

    * language (string): this defines which dictionary to use, it defaults to en_US - change this as required


    Warning: this requires the PyEnchant library to be installed 
    """
    def __init__(self, order=0):
        super(SpellingCorrectingModifier, self).__init__(order=order)
        self._use_language(Languages.ENGLISH_UK)

    def _use_language(self, language):
        self.language = language
        try:
            import enchant
        except ImportError:
            raise ImportError('enchant is not installed')

        self._spell_dict = enchant.Dict(self.language)
        return self

    def for_language(self, language):
        return SpellingCorrectingModifier(self.order)._use_language(language)

    @ensure_query
    def modify(self, query):
        def replace_misspelled(term):
            if not self._spell_dict.check(term):
                return self._spell_dict.suggest(term)[0]

            return term

        return ' '.join(map(replace_misspelled, query.tokenize()))
