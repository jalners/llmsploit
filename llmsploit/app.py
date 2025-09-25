from llmsploit.config_manager import ConfigManager
from llmsploit.request_manager import RequestManager
from llmsploit.scanner import Scanner
from llmsploit.evaluator import Evaluator
from llmsploit.imeca_analyzer import IMECAAnalyzer

class App:
    """
    Class for creating LLMsploit application.

    This class combines the functionality of all other code.
    """
    def __init__(self, path_or_config):
        """
        Initializes a new instance of LLMsploit App.

        Args:
            path_or_config (str | dict): The path to the application configuration file or configuration dictionary.
        """
        self.config_manager = ConfigManager()
        self._config = self.config_manager.create(path_or_config)

        self._request_manager = RequestManager()

        self._scanner = Scanner(self._request_manager, self._config["target"])
        self._evaluator = Evaluator(self._request_manager, self._config["evaluation"])
        self._analyzer = IMECAAnalyzer()

    def process(self):
        """
        Starts the LLM vulnerability scanning process.
        """
        self.check_connection()

        scan_result = self._scanner.scan()
        self._evaluator.evaluate(scan_result)
        analisis_result = self._analyzer.analyze(scan_result)

    def check_connection(self):
        """
        Checks the possibility of connecting to LLMs.
        """
        self._scanner.check_connection()
        self._evaluator.check_connection()
