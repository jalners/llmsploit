from pathlib import Path
from llmsploit.app import App

# Select the configuration for connecting to the target LLM after pre-configuring it.
targetConfigPath = Path(__file__).parent / "examples/docker_config.yaml"

# Select the configuration for connecting to the evaluation LLM after pre-configuring it.
evaluationConfigPath = Path(__file__).parent / "examples/docker_config.yaml"

# Create an application for future use.
app = App(targetConfigPath, evaluationConfigPath)

# Verifying connection to the LLM.
app.check_connection()

# For the complete vulnerability scanning process, call the following method:
# app.process()
