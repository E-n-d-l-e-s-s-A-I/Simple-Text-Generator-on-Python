import tkinter as tk
from tkinter import ttk

from model.file_handler import FileHandler


class MainWindow(tk.Tk):
    """
    Class describing main window.
    Attributes:
    _output_frame (ttk.Frame): frame with widgets where output data will be displayed:
        _output (tk.Text): widget where output data will be displayed.

    _input_frame (ttk.Frame): frame for user interaction:
        _generate_frame (ttk.Frame): frame for user interaction with generation.
            _generate_entry (tk.Entry): text input field for generation request.
            _generate_button (tk.Button): text generation button.

        _dictionaries_frame (ttk.Frame): frame for user interaction with selected dictionary.
            _dictionaries_combobox (ttk.Combobox): combobox for dictionary selection.
            _dictionary_name_entry (ttk.Entry): text input field for new dictionary name.
            _add_dictionary_button (tk.Button): button for adding a new dictionary.
            _delete_dictionary_button (tk.Button): button for delete a new dictionary.

        _update_frame (ttk.Frame): frame for update selected dictionary:
            _file_button (ttk.Radiobutton):  button that switches reading mode to reading file.
            _site_button (ttk.Radiobutton): button that switches reading mode to parsing site.

            _read_frame (ttk.Frame): frame for reading from a file/site:
                _read_label (ttk.label): label with name of current input mode.
                _read_entry (tk.Entry): field for entering a path to read.
                _read_site_button (tk.Button): button for reading site.
                _read_file_button (tk.Button): button for reading file.

    _image_frame (ttk.Frame): frame wirh a picture.

    mode (StringVar): variable showing current reading mode.
    """
    _output_width = 60  # width of output window in characters

    def __init__(self, output_width: int, image_name: str):
        super().__init__()
        self.geometry("1000x400")
        self.resizable(False, False)
        self.title("Text Generator")
        self._output_width = output_width
        self._image_name = image_name
        MainWindow._set_styles()
        self._set_ui()

    @property
    def input_mode(self) -> str:
        """Get current input mode."""
        return self._input_mode.get()

    @classmethod
    def get_output_width(self) -> int:
        return self._output_width

    def _set_ui(self) -> None:
        """Set and fill ui."""
        # set a top-level grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1, minsize=200)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # set frame and its contents in each grid cell
        self._set_output_frame()
        self._set_input_frame()
        self._set_image_frame()

    def _set_output_frame(self) -> None:
        """Set and fill output_frame."""
        self._output_frame = ttk.Frame(self, height=225, style="My.TFrame", width=700)
        self._output_frame.pack_propagate(False)
        self._output_frame.grid(row=0, column=0, sticky="nsew")

        self._output = tk.Text(self._output_frame, height=10, bg="#1E1E1E", fg="#E0E0E0", width=self._output_width)
        self._output.config(state='disabled')
        self._output.pack(padx=30, pady=50)

    def _set_input_frame(self) -> None:
        """Set and fill input_frame."""
        self._input_frame = ttk.Frame(self, style="My.TFrame")
        self._input_frame.grid(row=1, column=0, sticky="nsew")
        # set grid
        self._input_frame.grid_rowconfigure(0, weight=1)
        self._input_frame.grid_columnconfigure(0, weight=1)
        self._input_frame.grid_columnconfigure(1, weight=1)
        self._input_frame.grid_columnconfigure(2, weight=1)

        # set the frame and its contents in each grid cell
        self._set_generate_frame()
        self._set_dictionaries_frame()
        self._set_update_frame()

    def _set_generate_frame(self) -> None:
        """Set and fill generate_frame."""
        self._generate_frame = ttk.LabelFrame(self._input_frame, text="Generate", style="My.TLabelframe")
        self._generate_frame.grid(row=0, column=0, sticky="nsew")

        self._generate_button = MainWindow._set_button(self._generate_frame, "Сгенерировать")

        self._generate_entry = MainWindow._set_entry(self._generate_frame)

        ttk.Label(self._generate_frame, text="Введите начало фразы",
                  style="My.TLabel").pack(side="bottom", padx=20, pady=5)

    def _set_dictionaries_frame(self) -> None:
        """Set and fill dictionaries_frame."""
        self._dictionaries_frame = ttk.LabelFrame(self._input_frame, text="Dictionaries", style="My.TLabelframe")
        self._dictionaries_frame.grid(row=0, column=1, sticky="nsew")
        self._delete_dictionary_button = MainWindow._set_button(self._dictionaries_frame,
                                                                "Удалить выбранный",
                                                                )
        self._add_dictionary_button = MainWindow._set_button(self._dictionaries_frame, "Добавить", pady=0)
        self._dictionary_name_entry = MainWindow._set_entry(self._dictionaries_frame, pady=5)

        self._dictionaries_combobox = ttk.Combobox(self._dictionaries_frame,
                                                   state="readonly",
                                                   values=[file for file in FileHandler.get_files()]
                                                   )

        ttk.Label(self._dictionaries_frame, text="Выберете словарь", style="My.TLabel").pack(side="top")
        self._dictionaries_combobox.pack(side="top")

    def _set_update_frame(self) -> None:
        """Set and fill update_frame."""
        self._update_frame = ttk.LabelFrame(self._input_frame, text="Update", style="My.TLabelframe")
        self._update_frame.grid(row=0, column=2, sticky="nsew")

        self._read_file_button = MainWindow._set_button(self._update_frame, "Выберите файл", command=None)

    def _set_image_frame(self) -> None:
        """Set and fill image_frame."""
        self.image = tk.PhotoImage(file=self._image_name + ".png")

        self.image_frame = ttk.Frame(self, style="My.TFrame")
        self.image_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")

        self.image_label = ttk.Label(self.image_frame, image=self.image, style="My.TLabel")
        self.image_label.pack(expand=True)

    @staticmethod
    def _set_button(master, text: str, command=None, pady=10) -> tk.Button:
        """Create and pack and return button."""
        button = tk.Button(master,
                           text=text,
                           bg="#BB86FC",
                           command=command,
                           fg="#121212",
                           width=17,
                           )
        button.pack(side="bottom", pady=pady)
        return button

    @staticmethod
    def _set_entry(master, pady=0) -> tk.Entry:
        """Create and pack and return entry."""
        entry = tk.Entry(master, bg="#1E1E1E", fg="#E0E0E0")
        entry.pack(side="bottom", pady=pady)
        return entry

    @staticmethod
    def _set_styles() -> None:
        """Set styles."""
        styles = ttk.Style()
        styles.configure("My.TFrame", background="#121212")
        styles.configure("My.TLabelframe", background="#121212")
        styles.configure("My.TLabelframe.Label",
                         background="#121212",
                         foreground="#FFFFFF",
                         font=("Roboto", 14, "bold"))
        styles.configure("My.TLabel", background="#121212", foreground="#B0B0B0", font=("Roboto", 8))
        styles.configure("My.TRadiobutton", background="#121212", foreground="#B0B0B0", font=("Roboto", 8))

    def update_output(self, text: str) -> None:
        """Update contents of output widget."""
        self._output.config(state="normal")
        self._output.insert(tk.END, text)
        self._output.config(state="disabled")

    def clear_output(self) -> None:
        """Clear contents of output widget."""
        self._output.config(state="normal")
        self._output.delete(1.0, tk.END)
        self._output.config(state="disabled")

    def set_generate_command(self, command) -> None:
        """Set handler for generation button."""
        self._generate_button.config(command=command)

    def get_generate_entry(self) -> str:
        """Return content of input field to generate."""
        return self._generate_entry.get()

    def get_read_entry(self) -> str:
        """Return content of input path field."""
        return self._read_entry.get()

    def set_read_file_command(self, command) -> None:
        """Set handler for button to read from file."""
        self._read_file_button.config(command=command)

    def set_change_dictionary_command(self, command) -> None:
        """Set handler for button to change current dictionary."""
        self._dictionaries_combobox.bind("<<ComboboxSelected>>", command)

    def get_dictionary_name_entry(self) -> str:
        """Return content of dictionary name path field."""
        return self._dictionary_name_entry.get()

    def clear_dictionary_name_entry(self) -> None:
        """Clear content of dictionary name path field."""
        return self._dictionary_name_entry.delete(0, tk.END)

    def set_add_dictionary_button_command(self, command) -> None:
        """Set handler for button to add new dictionary."""
        self._add_dictionary_button.config(command=command)

    def set_delete_dictionary_button_command(self, command) -> None:
        """Set handler for button to delete selected dictionary."""
        self._delete_dictionary_button.config(command=command)

    def set_current_dict_combobox(self, current: str) -> None:
        """Return name of selected dictionary."""
        index = self.get_dict_combobox_values().index(current)
        self._dictionaries_combobox.current(index)

    def get_dict_combobox_values(self) -> list[str]:
        """Return list of dictionaries name from combobox."""
        return list(self._dictionaries_combobox["values"])

    def add_to_dict_combobox(self, value: str) -> None:
        """Add dictionary name to combobox."""
        self._dictionaries_combobox["values"] = self.get_dict_combobox_values() + [value]

    def get_selected_dict_combobox(self) -> str:
        """Return selected dictionary name from combobox."""
        return self.get_dict_combobox_values()[self._dictionaries_combobox.current()]

    def remove_in_dict_combobox(self, value: str) -> str:
        """Remove selected dictionary name from combobox and return new selected dictionary name."""
        dict_combobox_values = self.get_dict_combobox_values()
        dict_combobox_values.remove(value)
        self._dictionaries_combobox["values"] = dict_combobox_values
        if len(dict_combobox_values) > 0:
            self.set_current_dict_combobox(dict_combobox_values[0])
            return dict_combobox_values[0]
        else:
            self._dictionaries_combobox.set("")
            return ""
