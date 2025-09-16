from llmsploit.config_manager import ConfigManager
from llmsploit.request_manager import RequestManager
from llmsploit.scanner import Scanner
from llmsploit.evaluator import Evaluator

class App:
    """
    Class for creating LLMsploit application.

    This class combines the functionality of all other code.
    """
    def __init__(self, targetPath, evaluationPath):
        """
        Initializes a new instance of LLMsploit App.

        Args:
            targetPath (str): The path to the target LLM configuration file.
            evaluationPath (str): The path to the evaluation LLM configuration file.
        """
        self.config_manager = ConfigManager()

        self._target_config = self.config_manager.create_config(targetPath)
        self._evaluation_config = self.config_manager.create_config(evaluationPath)

        self._request_manager = RequestManager()

        self._scanner = Scanner(self._request_manager, self._target_config)
        self._evaluator = Evaluator(self._request_manager, self._evaluation_config)

    def process(self):
        """
        Starts the LLM vulnerability scanning process.
        """
        self.check_connection()
        self._scanner.scan()
        self._evaluator.evaluate()

    def check_connection(self):
        """
        Checks the possibility of connecting to LLMs.
        """
        self._scanner.check_connection()
        self._evaluator.check_connection()
