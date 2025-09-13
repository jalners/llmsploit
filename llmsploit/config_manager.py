import yaml
import os

class ConfigManager:
    """
    Class for managing application configuration.

    This class loads the configuration if it exists, validates for the required fields, and returns it.
    """
    def __init__(self):
        """
        Initializes a new instance of ConfigManager.
        """
        self._required_fields = ["url", "payload"]
        self._response_content = ["choices", 0, "message", "content"]

    def create_config(self, path):
        """
        Returns the configuration file.

        Args:
            path (str): The path to the configuration file.

        Returns:
            dict: A configuration file.
        """
        config = self._load(path)
        self._validate(config)
        self._set_headers(config)
        self._set_api_key(config)
        self._set_response_content(config)

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
            if not item in config:
                raise Exception(f"Required field '{item}' is not found in the configuration.")

    def _set_headers(self, config):
        """
        Sets the response headers field if it is missing.

        Args:
            config (dict): The configuration file.
        """
        if not "headers" in config:
            config["headers"] = {}

    def _set_api_key(self, config):
        """
        Sets the API key in headers if required.

        Args:
            config (dict): The configuration file.

        Raises:
            ValueError: If API key environment variable is not set.
        """
        if "api_key_name" in config:
            api_key = os.environ.get(config["api_key_name"])

            if api_key is None:
                raise ValueError(f"{config["api_key_name"]} environment variable is not set.")

            for key, value in config["headers"].items():
                config["headers"][key] = value.replace("{{api_key}}", api_key)

    def _set_response_content(self, config):
        """
        Sets the response process field if it is missing.

        Args:
            config (dict): The configuration file.
        """
        if not "response_content" in config:
            config["response_content"] = self._response_content
