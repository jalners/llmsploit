from llmsploit.app import App

# Configuration dictionary.
config = {
    "target_url": "http://localhost:12434/engines/v1/chat/completions",
    "target_model_name": "ai/gemma3",
    "evaluation_url": "http://localhost:12434/engines/v1/chat/completions",
    "evaluation_model_name": "ai/gpt-oss"
}

# Create an application for future use (with the configuration dictionary).
app = App(config)

# Create an application for future use (with path to the configuration file).
# app = App("example_config.yaml")

# Verifying connection to the LLM.
app.check_connection()

# For the complete vulnerability scanning process, call the following method:
# app.process()
