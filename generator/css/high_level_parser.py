import tinycss2


class CSSSizingParser:
    def __init__(self):
        self.rules = []

    def add_stylesheet(self, sheet_str: str):
        new_rules = tinycss2.parse_stylesheet(sheet_str)
        self.rules.extend(new_rules)


