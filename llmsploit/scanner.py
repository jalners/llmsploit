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

    def scan(self):
        """
        Scans LLM for vulnerabilities.
        """
        print("Scan")

    def check_connection(self):
        """
        Checks connection to the LLM.
        """
        self._request_manager.check_connection(self._config)
