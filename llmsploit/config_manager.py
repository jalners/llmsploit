import yaml
import os

class ConfigManager:
    """
    Manages application configuration.

    The manager loads the configuration if it exists and it is necessary,
    validates for the required fields, and returns it.
    """
    def __init__(self):
        """
        Initializes a new instance of ConfigManager.
        """
        self._required_fields = ["target_url", "target_model_name", "evaluation_url", "evaluation_model_name"]
        self._scheme = {
            "target_url": { "field": "target", "name": "url" },
            "target_model_name": { "field": "target", "name": "model_name" },
            "target_model_type": { "field": "target", "name": "model_type"},
            "target_api_key": { "field": "target", "name": "api_key", "default": "" },
            "categories": { "field": "target", "name": "categories" },
            "language": { "field": "target", "name": "language", "default": "en" },
            "exploits": { "field": "target", "name": "exploits" },
            "evaluation_url": { "field": "evaluation", "name": "url" },
            "evaluation_model_name": { "field": "evaluation", "name": "model_name" },
            "evaluation_model_type": { "field": "evaluation", "name": "model_type" },
            "evaluation_api_key": { "field": "evaluation", "name": "api_key", "default": "" }
        }

    def create(self, path_or_config):
        """
        Returns the configuration file.

        Args:
            path_or_config (str | dict): The path to the configuration file or configuration dictionary.

        Returns:
            dict: A configuration file.
        """
        config = path_or_config if isinstance(path_or_config, dict) else self._load(path_or_config)
        self._validate(config)
        self._set_api_keys(config)
        config = self._organize(config)

        return config

    def _load(self, path):
        """
        Loads the configuration file if it exists and saves in the internal field.

        Args:
            path (str): The path to the configuration file.

        Returns:
            dict: A raw configuration file.

        Raises:
            Exception: If configuration file is not exists.
            Exception: If a YAML file parsing error occurs.
        """
        try:
            with open(path, "r") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise Exception("Configuration file is not exists.")
        except yaml.YAMLError as e:
            raise Exception(f"Error parsing YAML: {e}")

    def _validate(self, config):
        """
        Validates configuration for the required fields.

        Args:
            config (dict): The configuration file.

        Raises:
            Exception: If one of required field is not found in the configuration.
        """
        for item in self._required_fields:
            if item not in config:
                raise Exception(f"Required field '{item}' is not found in the configuration.")

    def _set_api_keys(self, config):
        """
        Sets the API keys if required.

        Args:
            config (dict): The configuration file.

        Raises:
            ValueError: If API key environment variable is not set.
        """
        if "target_model_type" in config:
            target_api_key = os.environ.get(f"{config["target_model_type"].upper()}_API_KEY")

            if target_api_key is None:
                raise ValueError(f"{config["target_model_type"].upper()}_API_KEY environment variable is not set.")
            config["target_api_key"] = target_api_key

        if "evaluation_model_type" in config:
            evaluation_api_key = os.environ.get(f"{config["evaluation_model_type"].upper()}_API_KEY")

            if evaluation_api_key is None:
                raise ValueError(f"{config["evaluation_model_type"].upper()}_API_KEY environment variable is not set.")
            config["evaluation_api_key"] = evaluation_api_key

    def _organize(self, config):
        """
        Organizes configuration in accordance with the existing scheme.

        Args:
            config (dict): The configuration file.

        Returns:
            dict: An organized configuration.
        """
        result = {
            "target": {},
            "evaluation": {}
        }

        for key, value in self._scheme.items():
            if key in config:
                result[value["field"]][value["name"]] = config[key]
            elif "default" in value:
                result[value["field"]][value["name"]] = value["default"]

        return result
