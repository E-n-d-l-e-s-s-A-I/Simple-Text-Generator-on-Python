"""Module tests methods from TextGenerator and Ngram classes."""

from typing import Counter
import unittest

from model.ngram import Ngram
from model.text_generator import TextGenerator


class TestContinuePhrase(unittest.TestCase):
    def test_with_empty_input(self):
        ngrams = {}
        text_generaotor = TextGenerator(ngrams)
        with self.assertRaises(ValueError):
            text_generaotor.continue_phrase("")

    def test_do_nothing_on_empty_dictionary(self):
        ngrams = {}
        test_cases = ["x.", "a b c."]
        text_generaotor = TextGenerator(ngrams)
        [
            self.assertEqual(text_generaotor.continue_phrase(phrase_begin), phrase_begin)
            for phrase_begin in test_cases
        ]

    def test_one_bigram(self):
        ngrams = {
           "x": Ngram(text="x", most_frequently_continuations_list=["y"]),
        }
        text_generaotor = TextGenerator(ngrams)
        expected = "x y."
        actual = text_generaotor.continue_phrase("x")
        self.assertEqual(actual, expected)

    def test_continue_phrase_when_no_trigrams(self):
        ngrams = {
            "x": Ngram(text="x", most_frequently_continuations_list=["y"]),
            "y": Ngram(text="y", most_frequently_continuations_list=["z"]),
        }
        text_generaotor = TextGenerator(ngrams)
        test_cases = [
            ("x", "y z."),
            ("y", "z."),
        ]
        for phrase_begin, expected_new_words in test_cases:
            expected = phrase_begin+" "+expected_new_words
            actual = text_generaotor.continue_phrase(phrase_begin)
            self.assertEqual(actual, expected)

    def test_continue_phrase(self):
        ngrams = {
            "x": Ngram(text="x", most_frequently_continuations_list=["y"]),
            "x y": Ngram(text="x y", most_frequently_continuations_list=["z"]),
            "y": Ngram(text="x y", most_frequently_continuations_list=["q"]),
        }
        text_generaotor = TextGenerator(ngrams)
        test_cases = [
            ("x", "x y z."),
            ("x", "x y z."),
            ("x y", "x y z."),
            ("x x", "x x y z."),
            ("y x", "y x y z."),
            ("y y", "y y q."),
            ("y z", "y z."),
            ("a b x y", "a b x y z."),
            ("a b y", "a b y q."),
            ("y", "y q."),
        ]
        for phrase_begin, expected in test_cases:
            actual = text_generaotor.continue_phrase(phrase_begin)
            self.assertEqual(actual, expected)

    def test_continue_phrase_with_trigrams(self):
        ngrams = {
            "x": Ngram(text="x", most_frequently_continuations_list=["y"]),
            "x y": Ngram(text="x y", most_frequently_continuations_list=["z"]),
            "y z": Ngram(text="y z", most_frequently_continuations_list=["w"]),
            "z w": Ngram(text="z w", most_frequently_continuations_list=["v"]),
            "y": Ngram(text="y", most_frequently_continuations_list=["a"]),
            "z": Ngram(text="z", most_frequently_continuations_list=["b"]),
        }
        text_generaotor = TextGenerator(ngrams)
        expected = "x y z w v."
        actual = text_generaotor.continue_phrase("x y")
        self.assertEqual(actual, expected)

    def test_continue_phrase_with_multiletter_words(self):
        ngrams = {
            "hello": Ngram(text="hello", most_frequently_continuations_list=["everybody"]),
            "everybody be": Ngram(text="everybody be", most_frequently_continuations_list=["cool"]),
            "everybody": Ngram(text="everybody", most_frequently_continuations_list=["be"]),
        }
        text_generaotor = TextGenerator(ngrams)
        test_cases = [
            ("x.", ""),
            ("hello", "everybody be cool."),
            ("hello everybody", "be cool."),
            ("hello everybody be", "cool."),
            ("everybody be", "cool."),
            ("be.", ""),
            ("goodbye.", ""),
            ("be cool.", ""),
        ]
        for phrase_begin, expected_new_words in test_cases:
            expected = phrase_begin + " " + expected_new_words if expected_new_words else phrase_begin
            actual = text_generaotor.continue_phrase(phrase_begin)
            self.assertEqual(actual, expected)

    def test_continue_phrase_when_cycle_in_dictionary(self):
        ngrams = {
            "x": Ngram(text="x", most_frequently_continuations_list=["x"]),
            "y": Ngram(text="y", most_frequently_continuations_list=["x"]),
        }
        text_generaotor = TextGenerator(ngrams)
        test_cases = [
            ("x", " x" * TextGenerator._max_generated_word_count+"."),
            ("y", " x" * TextGenerator._max_generated_word_count+"."),
        ]
        for phrase_begin, expected_new_words in test_cases:
            expected = expected = phrase_begin + expected_new_words
            actual = text_generaotor.continue_phrase(phrase_begin)
            self.assertEqual(actual, expected)

    def test_dot_continue_after_10_new_words(self):
        ngrams = {
            "x": Ngram(text="x", most_frequently_continuations_list=["x", "."]),
        }
        text_generaotor = TextGenerator(ngrams)
        expected = "x" + " x"*TextGenerator._generated_without_dot+"."
        actual = text_generaotor.continue_phrase("x")
        self.assertEqual(actual, expected)


class TestGetNextWordByStart(unittest.TestCase):

    def test_one_continue_in_dictionary(self):
        ngram = Ngram(text="a", most_frequently_continuations_list=["b"])
        expected = "b"
        actual1 = ngram.get_next_word_not_dot_is_possible()
        actual2 = ngram.get_next_word_dot_is_possible()
        self.assertEqual(actual1, expected)
        self.assertEqual(actual2, expected)

    def test_two_continue_in_dictionary(self):
        ngram = Ngram(text="a", most_frequently_continuations_list=["b", "c"])

        possible_values = set(["b", "c"])
        obtained_values1 = set()
        obtained_values2 = set()
        try_count = 100

        while (possible_values != obtained_values2 and possible_values != obtained_values1) or try_count > 0:
            obtained_values1.add(ngram.get_next_word_not_dot_is_possible())
            obtained_values2.add(ngram.get_next_word_dot_is_possible())
            try_count -= 1

        self.assertEqual(possible_values, obtained_values1)
        self.assertEqual(possible_values, obtained_values2)

    def test_dot_and_not_dot_is_possible(self):
        ngram = Ngram(text="a", most_frequently_continuations_list=["b", "."])
        actual1 = ngram.get_next_word_not_dot_is_possible()
        actual2 = ngram.get_next_word_dot_is_possible()
        self.assertEqual(actual1, "b")
        self.assertEqual(actual2, ".")


class TestUpdateDicts(unittest.TestCase):

    def test_empty_dicts(self):
        self.text_generaotor = TextGenerator()
        input_count_dict = {}
        self.text_generaotor.update_dicts_by_count_dict(input_count_dict)
        self.assertEqual(self.text_generaotor._ngrams_dict, {})

    def test_nothing_change_when_empty_dict(self):
        start_count_dict = {
            "a":
                {
                    "b": 1,
                    "c": 3,
                },
        }
        ngrams = {
            "a": Ngram(text="a", most_frequently_continuations_list=["c", "b"], count_dict=start_count_dict),
        }
        self.text_generaotor = TextGenerator(ngrams)
        input_count_dict = {}
        self.text_generaotor.update_dicts_by_count_dict(input_count_dict)
        self.assertEqual(self.text_generaotor._ngrams_dict, ngrams)

    def test_add_to_empty_dict(self):
        self.text_generaotor = TextGenerator()
        start_count_dict = {
            "a":
                {
                    "b": 1,
                    "c": 3,
                },
        }
        expected_ngrams = {
            "a": Ngram(text="a", most_frequently_continuations_list=["c", "b"], count_dict=start_count_dict["a"]),
        }
        self.text_generaotor.update_dicts_by_count_dict(start_count_dict)
        self.assertEqual(self.text_generaotor._ngrams_dict, expected_ngrams)

    def test_add_count_dict(self):
        start_count_dict = {"a": Counter(["b", "c", "c", "c"])}

        start_ngram = {"a": Ngram(text="a", count_dict=start_count_dict["a"])}
        input_count_dict = {
            "a":
                {
                    "b": 2,
                    "r": 3,
                },
            "c":
                {
                    "a": 1,
                    "b": 5,
                },
        }
        expected_count_dict = {
            "a":
                {
                    "b": 3,
                    "c": 3,
                    "r": 3,
                },
            "c":
                {
                    "a": 1,
                    "b": 5,
                },
        }
        expected_ngrams = {
            "a": Ngram(text="a", count_dict=expected_count_dict["a"]),
            "c": Ngram(text="c", count_dict=expected_count_dict["c"]),
            }
        self.text_generaotor = TextGenerator(start_ngram)
        self.text_generaotor.update_dicts_by_count_dict(input_count_dict)
        self.assertEqual(self.text_generaotor._ngrams_dict, expected_ngrams)
