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
        self._result = []

    def check_connection(self):
        """
        Checks connection to the LLM.
        """
        print("=== Checking connection to the scanner LLM started ===")

        self._request_manager.check_connection(self._config)

        print(">> Connection to the scanner LLM checked\n")

    def scan(self):
        """
        Scans LLM for vulnerabilities.

        Returns:
            dict: A scan results data.
        """
        self._load_forbidden_texts()
        self._load_exploits()
        self._run()

        return self._result

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

    def _run(self):
        """
        Runs scanning process.
        """
        if not self._forbidden_texts:
            print("There is no category of forbidden texts chosen.")
            return None

        print("=== Processing started ===")

        for exploit in self._exploits:
            for forbidden_item in self._forbidden_texts:
                for prompt in forbidden_item["prompts"]:
                    print(f"Forbidden category [{forbidden_item["category"]}], exploit [{exploit["name"]}] - processing...")
                    response = self._request_manager.post(self._config, exploit["template"].replace("{{prompt}}", prompt))
                    self._result.append({
                        "exploit": exploit["name"],
                        "category": forbidden_item["category"],
                        "severity": forbidden_item["severity"],
                        "prompt": prompt,
                        "response": response
                    })

        print(">> All forbidden texts processed")
