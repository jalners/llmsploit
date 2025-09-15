from pathlib import Path
import glob
import yaml

class Scanner:
    """
    Class for creating Scanner.

    This class scans LLM for vulnerabilities.
    """
    def __init__(self, request_manager, config):
        """
        Initializes a new instance of Scanner.

        Args:
            request_manager (RequestManager): The instance of the RequestManager.
            config (dict): The configuration of the target LLM.
        """
        self._request_manager = request_manager
        self._config = config
        self._forbidden_texts_glob = str(Path(__file__).parent / "data/forbidden_texts/*.y*ml")
        self._exploits_glob = str(Path(__file__).parent / "data/exploits/*.y*ml")
        self._forbidden_texts = []
        self._exploits = []

    def scan(self):
        """
        Scans LLM for vulnerabilities.
        """
        self.check_connection()
        self._load_data("_forbidden_texts_glob", "_forbidden_texts")
        self._load_data("_exploits_glob", "_exploits")

    def check_connection(self):
        """
        Checks connection to the LLM.
        """
        self._request_manager.check_connection(self._config)

    def _load_data(self, glob_path, save_to):
        """
        Loads the data necessary for the scanner to work.

        Args:
            glob_path (str): The path to the files for download.
            save_to (str): The field name for storing data.
        """
        files = glob.glob(getattr(self, glob_path))

        for file_path in files:
            data = self._read_yaml_file(file_path)
            if data is not None:
                getattr(self, save_to).append(data)

    def _read_yaml_file(self, path):
        """
        Reads a YAML file.

        Args:
            glob_path (str): The path to the file for download.

        Raises:
            Exception: If a file is not found.
            Exception: If a YAML file parsing error occurs.
        """
        try:
            with open(path, "r") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise Exception(f"File is not found: {path}")
        except yaml.YAMLError as e:
            raise Exception(f"Error loading YAML from {path}: {e}")
