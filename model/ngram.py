import random

from model.frequency_analyzer import FrequencyAnalyzer


class Ngram():
    """Class describing ngram."""

    def __init__(self, text, count_dict=None, most_frequently_continuations_list=None):
        """
        Initialize the class with text and optional count_dict and most_frequently_continued_list.

        The default values for count_dict are assigned for testing convenience.
        In a real-world scenario, this arguments should always be provided with actual data.
        """
        self._frequency_analyzer = FrequencyAnalyzer()
        self._text = text
        self._count_dict = count_dict
        self._most_frequently_continuations_list = (
            most_frequently_continuations_list
            if most_frequently_continuations_list
            else self._frequency_analyzer.get_2_most_frequently_continuation(count_dict)
        )

    def update_dicts(self, input_count_dict) -> None:
        """
        Adds the values of the input count dictionary to the values of current count dictionary
        then finds the new most frequent continuations.
        """
        self._count_dict += input_count_dict
        self._update_most_frequently_continued_list()

    def _update_most_frequently_continued_list(self):
        """Update the the most frequent continuations by current count_dict."""
        self._most_frequently_continuations_list = (
            self._frequency_analyzer.get_2_most_frequently_continuation(
                self._count_dict
            )
        )

    def get_next_word_dot_is_possible(self) -> str:
        """Return random one from the list of the most frequent continuations, but if possible a dot."""
        if "." in self._most_frequently_continuations_list:
            return "."
        else:
            return random.choice(self._most_frequently_continuations_list)

    def get_next_word_not_dot_is_possible(self) -> str:
        """Return random one from the list of the most frequent continuations, but if possible not a dot."""
        if "." not in self._most_frequently_continuations_list:
            return random.choice(self._most_frequently_continuations_list)
        elif self._most_frequently_continuations_list[0] != ".":
            return self._most_frequently_continuations_list[0]
        elif len(self._most_frequently_continuations_list) > 1:
            return self._most_frequently_continuations_list[1]
        else:
            return "."

    def __eq__(self, other) -> bool:
        """Ngrams are equal when their count dictionaries and most frequently continuations list are equal."""
        if isinstance(other, Ngram):
            return self._text == other._text and self._count_dict == other._count_dict and (
                self._most_frequently_continuations_list == other._most_frequently_continuations_list)
        return False
