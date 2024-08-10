import pickle
import os
import re


from model.text_generator import TextGenerator


class FileHandler:
    """Сlass describing static methods for working with the file system."""
    _dumps_folder_path = "model/data"   # relative path to the folder where model dumps are stored

    @staticmethod
    def read_file(file_name: str) -> str:
        """Read the entire file."""
        with open(file_name, 'r', encoding="UTF-8") as file:
            return file.read()

    @staticmethod
    def write_data(data: TextGenerator, filename: str) -> None:
        """Serialize  text generator to pcl file."""
        with open(FileHandler._dumps_folder_path+f"/{filename}.pkl", 'wb') as file:
            pickle.dump(data, file)

    @staticmethod
    def read_data(filename: str) -> TextGenerator:
        """Deserialize  text generator from pcl file."""
        with open(FileHandler._dumps_folder_path+f"/{filename}.pkl", 'rb') as file:
            return pickle.load(file)

    @staticmethod
    def get_files() -> list[str]:
        """Get list of file names from dumps folder."""
        directory_path = FileHandler._dumps_folder_path
        return [f.split(".")[0] for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

    @staticmethod
    def delete_file(filename) -> None:
        """Delete file indumps folder."""
        os.remove(FileHandler._dumps_folder_path+f"/{filename}.pkl")

    @staticmethod
    def read_config() -> dict[str, str]:
        """Read config from project root folder."""
        with open("config.txt", 'r') as file:
            return {
                key: value for key, value in [(match.group(1), match.group(2))
                                              for match in re.finditer(r"([a-zA-Z_]+)=([a-zA-Z0-9_]*)", file.read())]
                }

    @staticmethod
    def save_config(config: dict[str, any]) -> None:
        """Save config in project root folder."""
        with open("config.txt", 'w') as file:
            for key, value in config.items():
                file.write(f"{key}={value}\n")
