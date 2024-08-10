"""Module tests methods from the FrequencyAnalyzer class."""

import unittest

from model.frequency_analyzer import FrequencyAnalyzer


class TestCreateCountDict(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frequency_analyzer = FrequencyAnalyzer()

    def test_return_correct_result_on_text_with_one_bigram(self):
        text = [["a", "."]]
        expected = {
            "a": {".": 1},
        }
        actual = self.frequency_analyzer.create_count_dict(text)
        self.assertEqual(actual, expected)

    def test_return_correct_result_on_text_with_some_bigram(self):
        text = [["a", "b", "a", "b", "c", "."]]
        expected = {
            "a": {"b": 2},
            "b": {"a": 1, "c": 1},
            "c": {".": 1},
            "a b": {"a": 1, "c": 1},
            "b a": {"b": 1},
            "b c": {".": 1},
        }
        actual = self.frequency_analyzer.create_count_dict(text)
        self.assertEqual(actual, expected)

    def test_return_correct_result_on_text_with_some_trigrams(self):
        text = [["a", "b", "c", "a", "b", "c", "."]]
        expected = {
            "a": {"b": 2},
            "b": {"c": 2},
            "c": {"a": 1, ".": 1},
            "a b": {"c": 2},
            "b c": {"a": 1, ".": 1},
            "c a": {"b": 1},
        }
        actual = self.frequency_analyzer.create_count_dict(text)
        self.assertEqual(actual, expected)

    def test_return_correct_result_on_text_with_some_sentences(self):
        text = [["a", "b", "c", "."], ["a", "b", "a", "."]]
        expected = {
            "a": {"b": 2, ".": 1},
            "b": {"c": 1, "a": 1},
            "c": {".": 1},
            "a b": {"c": 1, "a": 1},
            "b c": {".": 1},
            "b a": {".": 1},
        }
        actual = self.frequency_analyzer.create_count_dict(text)
        self.assertEqual(actual, expected)


class TestGet2MostFrequentlyContinued(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.frequency_analyzer = FrequencyAnalyzer()

    def test_works_with_empty_dict(self):
        dictionary = {}
        actual = self.frequency_analyzer._get_2_most_frequently_continuation(dictionary)
        excepted = None
        self.assertEqual(actual, excepted)

    def test_works_with_another_type_dict(self):
        dictionary = 1
        with self.assertRaises(TypeError):
            self.frequency_analyzer._get_2_most_frequently_continuation("a", dictionary)

        dictionary = 1.1
        with self.assertRaises(TypeError):
            self.frequency_analyzer._get_2_most_frequently_continuation("a", dictionary)

        dictionary = True
        with self.assertRaises(TypeError):
            self.frequency_analyzer._get_2_most_frequently_continuation("a", dictionary)

    def test_works_with_one_element_dict(self):
        dictionary = {"a": 1}
        actual = self.frequency_analyzer._get_2_most_frequently_continuation(dictionary)
        excepted = ["a"]
        self.assertEqual(actual, excepted)

    def test_return_2_most_frequently(self):
        dictionary = {
                    "b": 2,
                    'a': 1,
                    "d": 4,
                    "c": 3,
                    }
        actual = self.frequency_analyzer._get_2_most_frequently_continuation(dictionary)
        excepted = ["d", "c"]
        self.assertEqual(actual, excepted)

    def test_return_lexicographically_first(self):
        dictionarys = [
            {
                "b": 2,
                'a': 1,
                "d": 4,
                "c": 3,
                "i": 4,
                "g": 1,
            },
            {
                "b": 2,
                'a': 1,
                "i": 4,
                "c": 3,
                "d": 4,
                "g": 1,
            },
            {
                "d": 4,
                "i": 4,
                "b": 2,
                'a': 1,
                "c": 3,
                "g": 1,
            },
            {
                "d": 4,
                "b": 2,
                'a': 1,
                "c": 3,
                "g": 1,
                "i": 4,
            },
            {
                "i": 4,
                "b": 2,
                'a': 1,
                "c": 3,
                "g": 1,
                "d": 4,

            },
        ]
        for dictionary in dictionarys:
            actual = self.frequency_analyzer._get_2_most_frequently_continuation(dictionary)
            excepted = ["d", "i"]
            self.assertEqual(actual, excepted)
