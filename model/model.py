from model.file_handler import FileHandler
from model.text_generator import TextGenerator


class Model:
    """Class describing model."""
    def __init__(self, file_name=""):
        """
        Initializes model.

        file_name is name of the currently open dictionary.
        """
        self._dictionary_name = file_name
        if file_name:
            self._text_generator = FileHandler.read_data(file_name)
            if self._text_generator._text_parser is None:
                self._text_generator = TextGenerator()
                self._dictionary_name = file_name

    @property
    def dictionary_name(self):
        return self._dictionary_name

    def _update_text_generator(self, text: str) -> None:
        """Update dictionaries inside text_generator."""
        self._text_generator.update_dicts_by_text(text)

    def read_and_update(self, path: str) -> None:
        """Read text file by path and update text_generator by it."""
        self._update_text_generator(FileHandler.read_file(path))
        self.save_model(self._dictionary_name)

    def save_model(self, file_name) -> None:
        """Saves generator of the current model in a file named file_name."""
        FileHandler.write_data(self._text_generator, file_name)

    def generate(self, input: str) -> str:
        """Generate text by input in text generator."""
        if self._dictionary_name:
            return self._text_generator.continue_phrase(input)

    def open_model(self, file_name) -> None:
        """Open text generator model by file_name of his dump."""
        self._text_generator = FileHandler.read_data(file_name)
        self._dictionary_name = file_name

    def create_new(self, file_name) -> None:
        """Create new text generator and save current."""
        self._dictionary_name = file_name
        self._text_generator = TextGenerator()
        self.save_model(file_name)

    def delete(self) -> None:
        """Delete current text generator and create empty."""
        if self.dictionary_name:
            FileHandler.delete_file(self._dictionary_name)
            self._dictionary_name = ""
            self._text_generator = None
