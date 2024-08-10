import re


class TextParser():

    DELIMITERS = r"[.!?;()]+"  # regular expression for delimiters between sentences
    WORD = r"[a-zа-я']+[,:]?"  # regular expression for words

    def _parse_sentences(self, text: str) -> list[str]:
        """
        Splits the text into an array of sentences by DELIMITERS.
        """
        sentences = re.split(TextParser.DELIMITERS, text)
        return [sentence.strip().lower() for sentence in sentences if sentence.strip()]

    def _parse_words(self, sentence: str) -> list[str]:
        """
        Generates an list of sentence words.
        """
        return re.findall(TextParser.WORD, sentence)

    def parse_text(self, text: str) -> list[list[str]]:
        """
        Generates list of sentences for the text, each of which is list of strings corresponding to words.
        A dot at the end of a sentence is considered a word and is always put down.
        """
        result = []
        for sentence in self._parse_sentences(text):
            parse_sentence = self._parse_words(sentence)
            parse_sentence.append(".")
            result.append(parse_sentence)
        return result
