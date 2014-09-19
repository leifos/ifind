from query_generators.base_generator import BaseQueryGenerator
from ifind.common.query_ranker import QueryRanker
from ifind.common.language_model import LanguageModel
from ifind.common.query_generation import SingleQueryGeneration
from ifind.common.smoothed_language_model import BayesLanguageModel

class SingleTermQueryGenerator(BaseQueryGenerator):

    def _generate_topic_language_model(self, topic):
        """
        Given a Topic object, returns a language model representation for the given topic.
        Override this method in inheriting classes to generate and return different language models.
        """
        topic_text = topic.title
        topic_background = topic.content

        document_extractor = SingleQueryGeneration(minlen=3, stopwordfile=self._stopword_file)
        document_extractor.extract_queries_from_text(topic_text)
        document_term_counts = document_extractor.query_count

        document_extractor.extract_queries_from_text(topic_background)

        background_term_counts = document_extractor.query_count

        title_language_model = LanguageModel(term_dict=document_term_counts)
        background_language_model = LanguageModel(term_dict=background_term_counts)
        topic_language_model = BayesLanguageModel(title_language_model, background_language_model, beta=10)
        return topic_language_model

    def generate_query_list(self, topic):
        """
        Given a Topic object, produces a list of query terms that could be issued by the simulated agent.
        """
        topic_text = topic.content
        topic_lang_model = self._generate_topic_language_model(topic)

        single_query_generator = SingleQueryGeneration(minlen=3, stopwordfile=self._stopword_file)

        single_query_list = single_query_generator.extract_queries_from_text(topic_text)

        query_ranker = QueryRanker(smoothed_language_model=topic_lang_model)
        query_ranker.calculate_query_list_probabilities(single_query_list)
        return query_ranker.get_top_queries(100)