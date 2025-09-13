class Evaluator:
    """
    Class for creating Evaluator.

    This class evaluate LLM vulnerabilities.
    """
    def __init__(self, request_manager, config):
        """
        Initializes a new instance of Evaluator.

        Args:
            request_manager (RequestManager): The instance of the RequestManager.
            config (dict): The configuration of the evaluation LLM.
        """
        self._request_manager = request_manager
        self._config = config

    def evaluate(self):
        """
        Evaluates LLM vulnerabilities.
        """
        print("Evaluate")

    def check_connection(self):
        """
        Checks connection to the LLM.
        """
        self._request_manager.check_connection(self._config)
