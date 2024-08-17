from typing import Dict

from model.frequency_analyzer import FrequencyAnalyzer
from model.ngram import Ngram
from model.text_parser import TextParser


class TextGenerator():
    """Class describing TextGenerator."""

    _max_generated_word_count = 10  # maximum number of words generated
    _generated_without_dot = 10  # number of generated words after which Generator tries to complete the sentence

    def __init__(self, ngrams: Dict[str, Ngram] = None):
        self._text_parser = TextParser()
        self._frequency_analyzer = FrequencyAnalyzer()
        self._ngrams_dict = ngrams if ngrams else {}

    @property
    def ngrams_dict(self):
        return self._ngrams_dict

    def update_dicts_by_text(self, text: str) -> None:
        """Parse text and update dictionaries in ngrams in _ngrams_dict by it."""
        parsed_text = self._text_parser.parse_text(text)
        input_count_dict = self._frequency_analyzer.create_count_dict(parsed_text)
        self.update_dicts_by_count_dict(input_count_dict)

    def update_dicts_by_count_dict(self, input_count_dict: Dict[str, Dict[str, int]]) -> None:
        """Udpdate dictionaries in ngrams in _ngrams_dict by input_count_dict."""
        for ngram in input_count_dict:
            if ngram not in self._ngrams_dict:
                self._ngrams_dict[ngram] = Ngram(text=ngram, count_dict=input_count_dict[ngram])
            else:
                self._ngrams_dict[ngram].update_dicts(input_count_dict[ngram])

    def continue_phrase(self, phrase_begin: str) -> str:
        """Generate the text based on the beginning of the phrase."""
        parsed_text = self._text_parser.parse_text(phrase_begin)
        if len(parsed_text) == 0:
            raise ValueError()
        parse_phrase_begin = parsed_text[-1][:-1]
        words_count = 0
        next_word = ""
        while next_word != "." and words_count < TextGenerator._max_generated_word_count:
            bigram_start = parse_phrase_begin[-1]
            trigram_start = " ".join(parse_phrase_begin[-2:])

            if trigram_start in self._ngrams_dict:
                if words_count < TextGenerator._generated_without_dot:
                    next_word = self._ngrams_dict[trigram_start].get_next_word_not_dot_is_possible()
                else:
                    next_word = self._ngrams_dict[trigram_start].get_next_word_dot_is_possible()
            elif bigram_start in self._ngrams_dict:
                if words_count < TextGenerator._generated_without_dot:
                    next_word = self._ngrams_dict[bigram_start].get_next_word_not_dot_is_possible()
                else:
                    next_word = self._ngrams_dict[bigram_start].get_next_word_dot_is_possible()
            else:
                break

            parse_phrase_begin.append(next_word)
            words_count += 1

        if next_word == '.':
            parse_phrase_begin = parse_phrase_begin[:-1]

        return ' '.join(parse_phrase_begin)+"."

    @classmethod
    def set_max_generated_word_count(cls, value: int) -> None:
        """set max generated word count"""
        cls._max_generated_word_count = value

    @classmethod
    def set_generated_without_dot(cls, value: int) -> None:
        """set generated_without_dot"""
        cls._generated_without_dot = value
