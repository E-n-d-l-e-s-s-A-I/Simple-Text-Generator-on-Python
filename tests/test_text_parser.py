"""Module tests methods from TextParser class."""

import unittest

from model.text_parser import TextParser


class TestParseText(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.text_parser = TextParser()

    def test_none_text(self):
        text = None
        with self.assertRaises(TypeError):
            self.text_parser.parse_text(text)

    def test_another_type_text(self):
        text = 1
        with self.assertRaises(TypeError):
            self.text_parser.parse_text(text)

        text = 1.1
        with self.assertRaises(TypeError):
            self.text_parser.parse_text(text)

        text = True
        with self.assertRaises(TypeError):
            self.text_parser.parse_text(text)

        text = [1, 2]
        with self.assertRaises(TypeError):
            self.text_parser.parse_text(text)

    def test_empty_text(self):
        text = ""
        expected = []
        actual = self.text_parser.parse_text(text)
        self.assertEqual(actual, expected)

    def test_return_correct_result_on_text_with_one_sentence_with_one_word(self):
        text = "abc"
        expected = [["abc", "."]]
        actual = self.text_parser.parse_text(text)
        self.assertEqual(actual, expected)

    def test_return_correct_result_on_text_with_one_sentence_with_two_words(self):
        text = "b c"
        expected = [["b", "c", "."]]
        actual = self.text_parser.parse_text(text)
        self.assertEqual(actual, expected)

    def test_return_correct_result_on_text_with_one_sentence_with_word_containing_apostrophe(self):
        text = "it's"
        expected = [["it's", "."]]
        actual = self.text_parser.parse_text(text)
        self.assertEqual(actual, expected)

    def test_correctly_parse_sentence_delimiters(self):
        text = "a.b!c?d;e(f)g;h"
        expected = [["a", "."], ["b", "."], ["c", "."], ["d", "."], ["e", "."], ["f", "."], ["g", "."], ["h", "."]]
        actual = self.text_parser.parse_text(text)
        self.assertEqual(actual, expected)

    def test_correctly_parse_special_characters(self):
        text = "b;\tc;\rd;\ne;\r\nf;\r\n\r\ng"
        expected = [["b", "."], ["c", "."], ["d", "."], ["e", "."], ["f", "."], ["g", "."]]
        actual = self.text_parser.parse_text(text)
        self.assertEqual(actual, expected)

    def test_correctly_parse_one_sentence_with_word_delimiter(self):
        delimeters = ["^", "#", "$", "-", "+", "1", "=", " ", "\t", "\n", "\r"]
        [self.assertEqual(self.text_parser.parse_text("x"+delimeter+"y"), [["x", "y", "."]])
         for delimeter in delimeters]

    def test_return_result_in_lower_case(self):
        text = "B.C.D."
        expected = [["b", "."], ["c", "."], ["d", "."]]
        actual = self.text_parser.parse_text(text)
        self.assertEqual(actual, expected)

    def test_ignore_leading_and_trailing_spaces(self):
        text = " B . C"
        expected = [["b", "."], ["c", "."]]
        actual = self.text_parser.parse_text(text)
        self.assertEqual(actual, expected)

    def test_not_return_empty_sentence(self):
        texts = ["..", "...!!?", ""]
        [self.assertEqual([],  self.text_parser.parse_text(text)) for text in texts]

    def test_works_with_russian_language(self):
        text = "Очень нагруженный смысловой нагрузкой текст. Второе предложение этого великого текста."
        expected = [
            ["очень", "нагруженный", "смысловой", "нагрузкой", "текст", "."],
            ["второе", "предложение", "этого", "великого", "текста", "."],
        ]
        actual = self.text_parser.parse_text(text)
        self.assertEqual(actual, expected)

    def test_correectly_parse_word_with_punctuation(self):
        text = "a, b:. a, a:  b,"
        expected = [["a,", "b:", "."], ["a,", "a:", "b,", "."]]
        actual = self.text_parser.parse_text(text)
        self.assertEqual(actual, expected)
