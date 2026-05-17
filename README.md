LLMsploit a vulnerability scanner for Large Language Models
===================================

> [!WARNING]
> Please note that this repository contains examples of harmful, unethical, illegal, offensive, or biased language. We apologize for any discomfort that may arise while reading such content.

## Table of contents

* [Installation](#installation)
* [Using LLM models](#using-llm-models)
* [Getting started](#getting-started)
* [Resources](#resources)
* [Context](#context)
* [License](#license)

## Installation

1. Clone the repository:

    ```bash
    git clone git@github.com:jalners/llmsploit.git
    ```

2. Go to the project folder:

    ```bash
    cd llmsploit
    ```

3. Install dependencies using [uv](https://docs.astral.sh/uv/):

    ```bash
    uv sync
    ```

## Using LLM models

Set the API keys in the environment variables to work with external LLMs:
- For OpenAI models - `OPENAI_API_KEY`
- For Anthropic models - `ANTHROPIC_API_KEY`
- For Google Gemini models - `GOOGLE_API_KEY`
- For XAI Grok models - `XAI_API_KEY`

If you want to use local models, you have several options for doing this:
- Install [Docker](https://www.docker.com/) and use their [Docker Model Runner](https://www.docker.com/blog/introducing-docker-model-runner/) functionality
- Install [Ollama](https://ollama.com/) and use their models
- Install [LM Studio](https://lmstudio.ai/) to run local AI models

> [!NOTE]
> At the moment, we support working with models through OpenAI-compatible APIs (interfaces designed to mimic the structure and functionality of OpenAI's API endpoints).

## Getting started

LLMsploit can be used in Python applications and via the command line interface (CLI).

### Using in Python

The following code will help integrate LLMsploit into a Python application:

```python
from llmsploit.app import App

# Configuration dictionary.
config = {
    "target_url": "TARGET_LLM_URL",
    "target_model_name": "TARGET_LLM_NAME",
    "target_model_type": "TARGET_LLM_TYPE", # If an external model is used.
    "evaluation_url": "EVALUATION_LLM_URL",
    "evaluation_model_name": "EVALUATION_LLM_NAME",
    "evaluation_model_type": "EVALUATION_LLM_TYPE"  # If an external model is used.
}

# Create an application for future use (with the configuration dictionary).
app = App(config)

# Create an application for future use (with path to the configuration file).
# app = App("example_config.yaml")

# For the complete vulnerability scanning process, call the following method:
result = app.process()
```

If you have `Docker` and the `gemma3` and `gpt-oss` models installed, you can use the code examples from the `example.py` and `example_config.yaml` files.

### Using in CLI

Run the following command in your console:

```bash
uv run -m llmsploit --target_url TARGET_LLM_URL --target_model_name TARGET_LLM_NAME --evaluation_url EVALUATION_LLM_URL --evaluation_model_name EVALUATION_LLM_NAME
```

If you have `Docker` and the `gemma3` and `gpt-oss` models installed, you can Run the following command in your console:

```bash
uv run -m llmsploit --target_url http://localhost:12434/engines/v1/chat/completions --target_model_name ai/gemma3 --evaluation_url http://localhost:12434/engines/v1/chat/completions --evaluation_model_name ai/gpt-oss
```

### Application options description

- **target_url** - URL address of the investigated LLM
- **target_model_name** - Investigated LLM name
- **target_model_type** - Investigated LLM type (for external models only; possible values - `openai`, `anthropic`, `google`, `xai`, etc.)
- **categories** - Default forbidden categories for use (possible values - `"Harmful Content"`, `"Cybercrime Activities"`, `"Physical Harm"`, `"Economic Harm"`, `"Illegal Drugs"`, `"Weapons Activities"`, `"Terrorist Content"`, `"Intellectual Property Infringement"`, `"Fraud"`, `"Disinformation"`, `"Adult Content"`, `"Political Activities"`, `"Privacy Violations"`, `"Unauthorized Practices"`, `"Government Decisions"`)
- **exploits** - Exploit disabling flag (possible values - `False` for using in Python, empty value for CLI)
- **evaluation_url** - URL address of the evaluation LLM
- **evaluation_model_name** - Evaluation LLM name
- **evaluation_model_type** - Evaluation LLM type (for external models only; possible values - `openai`, `anthropic`, `google`, `xai`, etc.)

## Resources

See the RESOURCES.md file for more details about the list of used resources.

## Context

The scanner was developed while researching for a dissertation on competition for scientific degree of Doctor of Philosophy by specialty 125 Cybersecurity. – National Aerospace University "Kharkiv Aviation Institute", Kharkiv, 2026.

The theme of the dissertation is: "Methods and means of cybersecurity analysis and protection of Large Language Models from generating forbidden content on local and cloud servers".

Publications on the research topic:
- [Ensurance of artificial intelligence systems cyber security: analysis of vulnerabilities, attacks and countermeasures](https://science.lpnu.ua/sisn/all-volumes-and-issues/volume-12-2022/ensurance-artificial-intelligence-systems-cyber-security)
- [Model for Describing Processes of AI Systems Vulnerabilities Collection and Analysis using Big Data Tools](https://ieeexplore.ieee.org/document/10018811/)
- [Multi-source Analysis of AI Vulnerabilities: Methodology and Algorithms of Data Collection](https://ieeexplore.ieee.org/document/10348671)
- [Large Language Models Vulnerabilities Criticality: ІМЕСА-based Analysis of Attacks and Countermeasures](https://link.springer.com/chapter/10.1007/978-3-032-05802-7_34)
- [A model of ensuring LLM cybersecurity](https://nti.khai.edu/ojs/index.php/reks/article/view/reks.2025.2.13/2763)
- [Method for criticality analysis of vulnerabilities in Large Language Models](https://vottp.khmnu.edu.ua/index.php/vottp/article/view/786/769)
- [IMECA method of risk-based assessment and ensuring cybersecurity of Large Language Models](https://hait.od.ua/index.php/journal/article/view/238/204)
- [Information Technology for Assessing and Ensuring Cybersecurity of Large Language Models](https://journals.chnu.edu.ua/sisiot/article/view/1093/1094)

## License

This project is licensed under the MIT license. See the LICENSE file for more details.
