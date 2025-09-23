from pathlib import Path
import yaml

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
        self._judge_path = str(Path(__file__).parent / "data/judgement/judge.yaml")

    def check_connection(self):
        """
        Checks connection to the LLM.
        """
        self._request_manager.check_connection(self._config)

    def evaluate(self, data):
        """
        Evaluates LLM vulnerabilities.

        Args:
            data (dict): The scan results data.
        """
        self._load_judge()
        self._run(data)

    def _load_judge(self):
        """
        Loads a JUDGE file.

        Raises:
            Exception: If a file is not found.
            Exception: If a YAML file parsing error occurs.
        """
        try:
            with open(self._judge_path, "r") as file:
                self._judge = yaml.safe_load(file)
        except FileNotFoundError:
            raise Exception(f"File is not found: {self._judge_path}")
        except yaml.YAMLError as e:
            raise Exception(f"Error loading YAML from {self._judge_path}: {e}")

    def _run(self, data):
        """
        Runs evaluation process.

        Args:
            data (dict): The scan results data.
        """
        print("=== Evaluation started ===")

        for item in data:
            print(f"Forbidden category [{item["category"]}], exploit [{item["exploit"]}] - evaluation...")
            template = self._judge["template"].replace("{{prompt}}", item["prompt"])
            template = template.replace("{{response}}", item["response"])
            response = self._request_manager.post(self._config, template)
            item["Unsafe"] = response

        print(">> All assistant requests evaluated")
