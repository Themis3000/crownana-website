import dataclasses
import tinycss2
from tinycss2.ast import Node
from typing import Dict, List, Self


@dataclasses.dataclass
class SizingRule:
    widthPx: int | None
    heightPx: int | None

    def __post_init__(self):
        if self.widthPx is None and self.heightPx is None:
            raise Exception("Initiated SizingRule with empty height and width.")


@dataclasses.dataclass
class NamedSizingRule:
    name: str
    sizing_rule: SizingRule | None
    parent_rules: Dict[str, Self]

    def check_for_parent(self, parent_name: str) -> Self | None:
        return self.parent_rules.get(parent_name, None)

    def store_child(self, parent: Self):
        if parent.name in self.parent_rules:
            raise Exception("Duplicate rules detected... Uhhh whatdoido?")
        self.parent_rules[parent.name] = parent


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
                self._store_sizing_by_prelude(sizing_rule=sizing_rule, prelude=rule.prelude)
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

    def _store_sizing_by_prelude(self, sizing_rule: SizingRule, prelude: List[Node]):
        ###
        # The following need to be implemented
        # .thing .other-thing
        # selects all .other-thing in thing
        # .thing img
        # selects all img in .thing
        # .thing
        # #thing
        ####

        # Describes the inheritance of the name to be written out.
        # For example, prelude ".writing-style img" would turn into [".writing-style", img]
        name_inheritance_out = []

        prelude_iter = iter(prelude)
        for token in prelude_iter:
            # Skip all white spaces. No need to deal with them currently.
            # This removes the important distinction between .class1.class2 and .class1 .class2.
            # However, I don't utilize the former ever personally so this is no big deal for personal use.
            if isinstance(token, tinycss2.tokenizer.WhitespaceToken):
                continue

            # Is a comma token
            if isinstance(token, tinycss2.tokenizer.LiteralToken) and token.value == ",":
                self._store_sizing_by_prelude(sizing_rule=sizing_rule, prelude=list(prelude_iter))
                break

            # Cannot support an inheritance depth of more than 1 at this time.
            # It's unnecessary for the current scope to deal with.
            # Intentionally placed after the comma token check and whitespace check.
            if len(name_inheritance_out) == 2:
                break

            # Is a class definition
            if isinstance(token, tinycss2.tokenizer.LiteralToken) and token.value == ".":
                class_name_token = next(prelude_iter)
                if not isinstance(class_name_token, tinycss2.tokenizer.IdentToken):
                    raise Exception("Parsing error! Expected class name ident.")
                name_inheritance_out.append(f".{class_name_token.value}")
                continue

            # Is an id
            if isinstance(token, tinycss2.tokenizer.HashToken):
                name_inheritance_out.append(f"#{token.value}")
                continue

            # Is a bear ident (such as img)
            if isinstance(token, tinycss2.tokenizer.IdentToken):
                name_inheritance_out.append(token.value)
                continue
