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
        self._exploits = [{
            "name": "Default",
            "source": "",
            "template": "{{prompt}}"
        }]

    def scan(self):
        """
        Scans LLM for vulnerabilities.
        """
        self._load_forbidden_texts()
        self._load_exploits()

    def check_connection(self):
        """
        Checks connection to the LLM.
        """
        self._request_manager.check_connection(self._config)

    def _load_forbidden_texts(self):
        """
        Loads forbidden texts.
        """
        files = glob.glob(self._forbidden_texts_glob)

        for file_path in files:
            data = self._read_yaml_file(file_path)
            if data is not None and self._is_forbidden_data_required(data):
                self._forbidden_texts.append(data)

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

    def _is_forbidden_data_required(self, data):
        """
        Checks whether forbidden data needs to be filtered.

        Args:
            data (dict): The loaded forbidden data.

        Returns:
            bool: True if the data is required, False otherwise.
        """
        if "categories" not in self._config:
            return True
        if data["category"] in self._config["categories"]:
            return True
        if data["subcategory"] in self._config["categories"]:
            return True
        return False

    def _load_exploits(self):
        """
        Loads exploits.
        """
        files = glob.glob(self._exploits_glob)

        if self._is_exploits_data_required():
            for file_path in files:
                data = self._read_yaml_file(file_path)
                if data is not None:
                    self._exploits.append(data)

    def _is_exploits_data_required(self):
        """
        Checks whether exploits data needs to be filtered.

        Returns:
            bool: True if the data is required, False otherwise.
        """
        if "exploits" not in self._config:
            return True
        if self._config["exploits"] == True:
            return True
        return False
