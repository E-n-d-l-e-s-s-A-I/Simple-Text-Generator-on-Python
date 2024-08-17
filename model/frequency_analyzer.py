from collections import defaultdict, Counter
from typing import Dict, List


class FrequencyAnalyzer:
    """Class describing methods of frequency analysis."""

    def create_count_dict(self, text_list: List[List[str]]) -> Dict[str, Counter]:
        """Create a count dictionary by parsed text."""
        count_dictionary = defaultdict(Counter)
        for sentence_list in text_list:
            for i in range(len(sentence_list)-1):
                # обработка биграмм
                bigram_start = sentence_list[i]
                bigram_end = sentence_list[i+1]
                count_dictionary[bigram_start].update([bigram_end])
                # обработка триграмм
                if i < len(sentence_list)-2:
                    trigram_start = ' '.join(sentence_list[i:i+2])
                    trigram_end = sentence_list[i+2]
                    count_dictionary[trigram_start].update([trigram_end])

        return count_dictionary

    def get_2_most_frequently_continuation(self, count_dictionary:  Counter) -> List[str]:
        """Return two most frequent continuations by count dictionary."""
        iter_dict_keys = iter(count_dictionary.keys())
        if len(count_dictionary) == 0:
            return None
        if len(count_dictionary) == 1:
            return [next(iter_dict_keys)]
        else:
            first_elem_key = next(iter_dict_keys)
            second_elem_key = next(iter_dict_keys)
            if FrequencyAnalyzer._compare_count_dict_items(first_elem_key, second_elem_key, count_dictionary):
                max1 = first_elem_key
                max2 = second_elem_key
            else:
                max2 = first_elem_key
                max1 = second_elem_key

            for end in iter_dict_keys:
                if FrequencyAnalyzer._compare_count_dict_items(end, max1, count_dictionary):
                    max2 = max1
                    max1 = end
                elif FrequencyAnalyzer._compare_count_dict_items(end, max2, count_dictionary):
                    max2 = end
            return [max1, max2]

    @staticmethod
    def _compare_count_dict_items(key1, key2, dictionary) -> bool:
        """Compare two continuations by key in count dictionary."""
        value1 = dictionary[key1]
        value2 = dictionary[key2]
        if value1 > value2:
            return True
        else:
            return value1 == value2 and key1 < key2
