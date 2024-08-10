from tkinter import filedialog
import re

from view.main_window import MainWindow
from model.model import Model
from model.texts_methods import add_line_feed
from model.file_handler import FileHandler
from model.text_generator import TextGenerator


class Controller:
    """Class describing controller."""
    _default_config = {
        "current_dictionary": "",
        "output_width": 60,
        "start_interval": 50,
        "words_interval": 50,
        "phrase_interval": 1000,
        "max_generated_word_count": 30,
        "generated_without_dot": 10,
    }   # contains the default settings

    def __init__(self):
        self._config = self._read_config()

        TextGenerator.set_generated_without_dot(self._config["generated_without_dot"])
        TextGenerator.set_max_generated_word_count(self._config["max_generated_word_count"])

        self.model = Model(self._config["current_dictionary"])
        self.view = MainWindow(output_width=self._config["output_width"])
        self._set_controllers()

        self.view.mainloop()

    def _set_controllers(self) -> None:
        """Binds controller functions to handlers from the main window."""
        self.view.set_read_file_command(command=self._select_file)

        self.view.set_generate_command(self._generate)
        self.view.set_change_dictionary_command(self._dictionaries_combobox_selected)
        self.view.set_add_dictionary_button_command(self._add_dictionary)
        self.view.set_delete_dictionary_button_command(self._delete_dictionary)

        if self.model.dictionary_name:
            self.view.set_current_dict_combobox(self.model.dictionary_name)

        self.view.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _read_config(self) -> dict[str, str]:
        """Read and validate and return config. If anything wrong return default config."""
        try:
            read_config = FileHandler.read_config()
            return self._validate_config(read_config)
        except (TypeError):
            return Controller._default_config

    def _validate_config(self, config) -> dict[str, str]:
        """Validate and return the corrected config, according to the default config."""
        for key in set(Controller._default_config).difference(set(config)):
            config[key] = Controller._default_config[key]

        for option in ("output_width", "start_interval",
                       "words_interval", "phrase_interval",
                       "max_generated_word_count", "generated_without_dot"):
            if not all([symbol.isdigit() for symbol in config[option]]):
                config[option] = self._default_config[option]
            config[option] = int(config[option])

        if config["current_dictionary"] not in FileHandler.get_files():
            config["current_dictionary"] = self._default_config["current_dictionary"]

        return config

    def _print_output_message(self, text) -> None:
        """Print text to output of main window."""
        self.view.clear_output()
        self.view.update_output(add_line_feed(text))

    def _select_file(self) -> None:
        """Handler for clicking on the file selection button."""
        if self.model.dictionary_name:
            file_path = filedialog.askopenfilename()
            if file_path:
                try:
                    self._print_output_message("Идет обновление словаря...")
                    self.view.update()
                    self.model.read_and_update(file_path)
                except (UnicodeDecodeError):
                    self._print_output_message("Неверный тип файла")
                else:
                    self._print_output_message("Словарь обновлен")
        else:
            self._print_output_message("Словарь не открыт")

    def _generate(self) -> None:
        """Handler for clicking on the generate text button."""
        if self.model.dictionary_name:
            input = self.view.get_generate_entry()
            try:
                output = self.model.generate(input)
            except (ValueError):
                output = "В вводе должен быть хотя бы один литинский или кириллический символ"
            self._print_output_message(output)
        else:
            self._print_output_message("Словарь не открыт")

    def _dictionaries_combobox_selected(self, event) -> None:
        """Handler for selecting in the dictionaries combobox."""
        current_dict = self.view.get_selected_dict_combobox()
        if current_dict != self.model.dictionary_name:
            self.model.open_model(current_dict)

    def _add_dictionary(self) -> None:
        """Handler for clicking on the add dictionary button."""
        entry_file_name = self.view.get_dictionary_name_entry()
        match = re.match(r"[A-Za-z_]+", entry_file_name)
        if match is None or entry_file_name != match.group(0):
            self._print_output_message("недопустимое имя файла")
        elif entry_file_name in FileHandler.get_files():
            self._print_output_message("файл с таким именем уже существует")
        else:
            self.model.create_new(entry_file_name)
            self.view.add_to_dict_combobox(entry_file_name)
            self.view.set_current_dict_combobox(entry_file_name)
            self.view.clear_dictionary_name_entry()

    def _delete_dictionary(self) -> None:
        """Handler for clicking on the delete dictionary button."""
        if self.model.dictionary_name:
            current = self.view.remove_in_dict_combobox(self.model.dictionary_name)
            self.model.delete()
            if current:
                self.model.open_model(current)

    def _on_closing(self) -> None:
        """Handler for closing app."""
        self._config["current_dictionary"] = self.model.dictionary_name
        FileHandler.save_config(self._config)
        self.view.destroy()
