import argparse
from llmsploit.app import App

def run(arguments=None):
    """
    Runs the LLMsploit

    Args:
        arguments (list): The list of arguments passed by the user.
    """
    try:
        if arguments is None:
            arguments = []

        parser = argparse.ArgumentParser(
            prog="python -m llmsploit",
            description="LLMsploit a vulnerability scanner for Large Language Models",
            allow_abbrev=False,
        )

        parser.add_argument("--target_url", type=str, help="URL address of the investigated LLM")
        parser.add_argument("--target_model_name", type=str, help="Target LLM name")
        parser.add_argument("--target_model_type", type=str, help="Target LLM type", default=argparse.SUPPRESS)
        parser.add_argument("--categories", type=str, nargs="*", help="Allowed forbidden categories", default=argparse.SUPPRESS)
        parser.add_argument("--exploits", action="store_false", help="Exploit disabling flag", default=argparse.SUPPRESS)
        parser.add_argument("--evaluation_url", type=str, help="URL address of the evaluation LLM")
        parser.add_argument("--evaluation_model_name", type=str, help="Evaluation LLM name")
        parser.add_argument("--evaluation_model_type", type=str, help="Evaluation LLM type", default=argparse.SUPPRESS)

        args = parser.parse_args(arguments)
        config = vars(args)

        app = App(config)
        app.process()
    except KeyboardInterrupt as e:
        print("Processing canceled")
    except Exception as e:
        print(e)
