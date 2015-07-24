"""
Test suit for my snippet utilities
"""
import unittest
import utils

# TODO consider using py.test or nose
# Test fixture
doc = ''


class TestSnippetUtilities(unittest.TestCase):

    def setUp(self):
        global doc
        doc = utils.read_file('article.txt')

    def test_run_queries(self):
        pass

    def test_format_results(self):
        pass

    def test_analyse_snippets(self):
        pass

    def test_reduce_snippets(self):
        pass

    def test_remove_stopwords(self):
        snippet = 'The town in the states'
        filtered_snippet = ['town', 'states']
        self.assertItemsEqual(utils.remove_stopwords(snippet),
                              actual_seq=filtered_snippet,
                              msg='Removed stop words')

    def test_extract_entities(self):

        entities = utils.extract_entities(doc)

        expected_entities = {'Malware', 'US Federal Trade Commission',
                             'Symantec', 'Andrew Conway', 'Ransomware',
                             'Eastern Europe', 'Cloudmark', 'Ben Nahorney',
                             'China', 'UK', 'European'}

        self.assertSetEqual(entities, expected_entities)

    def test_import_term_frequency(self):
        pass

    def test_calc_term_frequency(self):

        term_freqs = utils.calc_term_frequency(doc)

        spam_freq = term_freqs['spam']
        actual_freq = 9
        self.assertEqual(spam_freq, actual_freq)

    def test_calc_term_probability(self):
        pass

    def test_gen_snippet(self):
        pass


if __name__ == '__main__':
    unittest.main()
