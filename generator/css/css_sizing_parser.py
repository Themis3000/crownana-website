import dataclasses
import tinycss2
from typing import Dict


@dataclasses.dataclass
class SizingRule:
    widthPx: int | None
    heightPx: int | None

    def __post_init__(self):
        if self.widthPx is None and self.heightPx is None:
            raise Exception("Initiated SizingRule with empty height and width.")


class CSSSizingParser:
    def __init__(self):
        self.classes: Dict[str, SizingRule] = {}
        self.ids: Dict[str, SizingRule] = {}
        self.idents: Dict[str, SizingRule] = {}

    def add_stylesheet(self, sheet_str: str):
        rules = tinycss2.parse_stylesheet(sheet_str, skip_whitespace=True, skip_comments=True)
        for rule in rules:
            if not isinstance(rule, tinycss2.parser.QualifiedRule):
                continue

            declarations = tinycss2.parse_blocks_contents(rule.content, skip_whitespace=True, skip_comments=True)
            width: int | None = None
            height: int | None = None
            for declaration in declarations:
                if not isinstance(declaration, tinycss2.parser.Declaration):
                    continue
                if declaration.lower_name == "width":
                    width = self._extract_px_dimension(declaration)
                    continue
                if declaration.lower_name == "height":
                    height = self._extract_px_dimension(declaration)

            if width or height:
                sizing_rule = SizingRule(widthPx=width, heightPx=height)
                print(sizing_rule)

    @staticmethod
    def _extract_px_dimension(declaration: tinycss2.parser.Declaration) -> int | None:
        token = tinycss2.parse_one_component_value(declaration.value, skip_comments=True)
        if not isinstance(token, tinycss2.tokenizer.DimensionToken):
            return
        if not token.is_integer:
            return
        if token.lower_unit != "px":
            return
        return token.int_value
