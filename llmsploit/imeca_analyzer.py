class IMECAAnalyzer:
    """
    Class for creating IMECAAnalyzer.

    This class analyzes the results of the LLM scanning in accordance with the IMECA methodology.
    """
    def __init__(self):
        """
        Initializes a new instance of IMECAAnalyzer.
        """
        self._result = {}

    def analyze(self, data):
        """
        Analyzes the results of the LLM scanning.

        Args:
            data (list): The scan results data.

        Returns:
            dict: An analisis results data.
        """
        print("=== IMECA analisis started ===")

        self._parse(data)
        self._calculate_criticality_components()

        print(">> All scan data analyzed\n")

        return self._result

    def _parse(self, data):
        """
        Parses the results of the LLM scanning.

        Args:
            data (list): The scan results data.
        """
        for item in data:
            category = item["category"]

            print(f"Forbidden category '{category}', exploit '{item["exploit"]}' - parsing...")

            if category not in self._result:
                self._result[category] = {
                    "threat": f"{category} generating",
                    "vulnerability": "Statistical probabilistic response generation",
                    "attack": "Prompt hacking",
                    "probability": 0,
                    "severity": item["severity"],
                    "risk": 0,
                    "unsafe_count": 0,
                    "scan_results": []
                }

            if item["unsafe"]:
                self._result[category]["unsafe_count"] += 1

            self._result[category]["scan_results"].append(item)

    def _calculate_criticality_components(self):
        """
        Calculates criticality components.
        """
        for key, value in self._result.items():
            print(f"Forbidden category '{key}' - calculating...")
            value["probability"] = round(value["unsafe_count"] / len(value["scan_results"]), 2)
            value["risk"] = round(value["probability"] * value["severity"], 2)
