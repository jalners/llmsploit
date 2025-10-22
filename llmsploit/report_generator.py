from pathlib import Path
import os
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader

class ReportGenerator:
    """
    Turns raw data into a structured report.

    The generator produces a report in HTML format.
    """
    def __init__(self, config):
        """
        Initializes a new instance of ReportGenerator.

        Args:
            config (dict): The application configuration.
        """
        self._config = config
        self._templates_path = str(Path(__file__).parent / "templates")
        self._template_name = "report.html"

    def generate(self, data, duration):
        """
        Generates the report.

        Args:
            data (list): The scan results data.
            duration (float): The scan duration.

        Returns:
            dict: A generated report.
        """
        report = self._create_report(data, duration)
        self._write_report(report)

        return report

    def _create_report(self, data, duration):
        """
        Creates the report.

        Args:
            data (list): The scan results data.
            duration (float): The scan duration.

        Returns:
            dict: A generated report.
        """
        report = {
            "scan_date": datetime.now().strftime("%d %b %Y %H:%M:%S"),
            "scan_duration": timedelta(seconds=round(duration)),
            "target_model_name": self._config["target"]["model_name"],
            "evaluation_model_name": self._config["evaluation"]["model_name"],
            "total_requests": 0,
            "total_unsafe_responses": 0,
            "categories": [],
            "exploits": [],
            "risk_matrix": { "ll": [], "lm": [], "lh": [], "ml": [], "mm": [], "mh": [], "hl": [], "hm": [], "hh": [] },
            "analysis": data
        }

        for index, (key, value) in enumerate(data.items()):
            report["total_requests"] += len(value["scan_results"])
            report["total_unsafe_responses"] += value["unsafe_count"]
            report["categories"].append(key)
            report["exploits"] = list(set(report["exploits"] + value["exploits"]))

            if value["probability"] > 0:
                report["risk_matrix"][value["risk_matrix"]].append(str(index + 1))

        return report

    def _write_report(self, report):
        """
        Writes the report to a file.

        Args:
            report (dict): The generated report.

        Raises:
            Exception: If an error occurred while writing report to the file.
        """
        try:
            env = Environment(loader=FileSystemLoader(self._templates_path))
            template = env.get_template(self._template_name)
            output = template.render(report=report)

            if not os.path.exists("reports"):
                os.makedirs("reports", exist_ok=True)

            with open(f"reports/report.{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.html", "w") as file:
                file.write(output)
        except Exception as e:
            raise Exception(f"An unexpected error occurred while writing report to the file: {e}")
