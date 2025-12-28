from llmsploit.config_manager import ConfigManager
from llmsploit.request_manager import RequestManager
from llmsploit.connection_checker import ConnectionChecker
from llmsploit.scanner import Scanner
from llmsploit.evaluator import Evaluator
from llmsploit.imeca_analyzer import IMECAAnalyzer
from llmsploit.report_generator import ReportGenerator
import time

class App:
    """
    The main entry point for the LLMsploit application.

    This class orchestrates the entire application lifecycle.
    """
    def __init__(self, path_or_config):
        """
        Initializes a new instance of LLMsploit App.

        Args:
            path_or_config (str | dict): The path to the application configuration file or configuration dictionary.
        """
        self._config_manager = ConfigManager()
        self._config = self._config_manager.create(path_or_config)

        self._request_manager = RequestManager()

        self._connection_checker = ConnectionChecker(self._request_manager, self._config)
        self._scanner = Scanner(self._request_manager, self._config["target"])
        self._evaluator = Evaluator(self._request_manager, self._config["evaluation"])
        self._analyzer = IMECAAnalyzer()
        self._report_generator = ReportGenerator(self._config)

    def process(self):
        """
        Starts the LLM vulnerability scanning process.

        Returns:
            dict: An analisis results data.
        """
        start_time = time.perf_counter()

        self._connection_checker.check()
        scan_result = self._scanner.scan()
        self._evaluator.evaluate(scan_result)
        analisis_result = self._analyzer.analyze(scan_result)

        end_time = time.perf_counter()

        report = self._report_generator.generate(analisis_result, end_time - start_time)

        return report
