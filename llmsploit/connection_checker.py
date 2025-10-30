class ConnectionChecker:
    """
    Checks connection to the LLMs.

    The checker sends prompt to the LLMs verifying that access to the models is possible.
    """
    def __init__(self, request_manager, config):
        """
        Initializes a new instance of ConnectionChecker.

        Args:
            request_manager (RequestManager): The instance of the RequestManager.
            config (dict): The application configuration.
        """
        self._request_manager = request_manager
        self._config = config

    def check(self):
        """
        Checks the possibility of connecting to LLMs.
        """
        self._run(self._config["target"], "scanner")
        self._run(self._config["evaluation"], "evaluator")

    def _run(self, config, type):
        """
        Checks the connection to the LLM.

        Args:
            config (dict): The LLM configuration.
            type (str): The type of the LLM.

        Raises:
            Exception: If connection to the LLM failed.
        """
        print(f"=== Checking connection to the {type} LLM started ===")

        response = self._request_manager.post(config, "What is the capital of France? Answer in English.")

        if ('paris' not in response.lower()):
            raise Exception(f"Connection to the '{config["model_name"]}' LLM failed.")

        print(f"Successful connection to the '{config["model_name"]}' LLM")
        print(f">> Connection to the {type} LLM checked\n")
