import dataclasses

import bs4
import tinycss2
from tinycss2 import tokenizer
from tinycss2.ast import Node
from typing import Dict, List, Self, Set


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
    parent_rules: Dict[str, Self] = dataclasses.field(default_factory=dict)

    def check_for_parent(self, parent_name: str) -> Self | None:
        return self.parent_rules.get(parent_name, None)

    def store_parent(self, parent: Self):
        if parent.name in self.parent_rules:
            raise Exception("Duplicate rules detected... Uhhh whatdoido?")
        self.parent_rules[parent.name] = parent


class CSSSizingParser:
    def __init__(self):
        self.sizing_rules: Dict[str, NamedSizingRule] = {}

    @staticmethod
    def _get_tag_lookup_names(tag: bs4.Tag) -> Set[str]:
        lookup_names = {tag.name}
        tag_id_attr = tag.get("id")
        if tag_id_attr is not None:
            lookup_names.add(f"#{tag_id_attr}")
        tag_class_attr = tag.get("class")  # bs4 automatically handles converting this into a list of classes.
        if tag_class_attr is not None:
            lookup_names.update([f".{class_name}" for class_name in tag_class_attr])
        return lookup_names

    def get_tag_size(self, tag: bs4.Tag) -> SizingRule | None:
        lookup_names = self._get_tag_lookup_names(tag)
        parent_lookup_names: Set[str] = set()
        for parent in tag.parents:
            parent_lookup_names.update(self._get_tag_lookup_names(parent))

        out_sizing_rules = []
        for name in lookup_names:
            named_sizing_rule = self.sizing_rules.get(name)
            if named_sizing_rule is None:
                continue
            if named_sizing_rule.sizing_rule is not None:
                out_sizing_rules.append(named_sizing_rule.sizing_rule)
            for parent_lookup_name in parent_lookup_names:
                parent_named_rule = named_sizing_rule.check_for_parent(parent_lookup_name)
                if parent_named_rule is None:
                    continue
                if parent_named_rule.sizing_rule is None:
                    raise Exception("Found parent... But it had no sizing rule. This is unexpected behavior.")
                out_sizing_rules.append(parent_named_rule.sizing_rule)

        if len(out_sizing_rules) > 1:
            # If this is raised, I should probably implement some way to determine which sizing rule to return.
            # The easy way would probably be to return whichever one is larger?
            # (but what if one has only height defined and the other only width)
            # I could fall back to no size found when conflicting values that only have a single distention found
            # is encountered.
            raise Exception("Conflicting sizing rules found!")
        if len(out_sizing_rules) == 0:
            return None
        return out_sizing_rules[0]

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

        print(self.sizing_rules)

    @staticmethod
    def _extract_px_dimension(declaration: tinycss2.parser.Declaration) -> int | None:
        token = tinycss2.parse_one_component_value(declaration.value, skip_comments=True)
        if not isinstance(token, tokenizer.DimensionToken):
            return
        if not token.is_integer:
            return
        if token.lower_unit != "px":
            return
        return token.int_value

    def _store_sizing_by_prelude(self, sizing_rule: SizingRule, prelude: List[Node]):
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
            if isinstance(token, tokenizer.LiteralToken) and token.value == ",":
                self._store_sizing_by_prelude(sizing_rule=sizing_rule, prelude=list(prelude_iter))
                break

            # Cannot support an inheritance depth of more than 1 at this time.
            # It's unnecessary for the current scope to deal with.
            # Intentionally placed after the comma token check and whitespace check.
            if len(name_inheritance_out) == 2:
                break

            # Is a class definition
            if isinstance(token, tokenizer.LiteralToken) and token.value == ".":
                class_name_token = next(prelude_iter)
                if not isinstance(class_name_token, tokenizer.IdentToken):
                    raise Exception("Parsing error! Expected class name ident.")
                name_inheritance_out.append(f".{class_name_token.value}")
                continue

            # Is an id
            if isinstance(token, tokenizer.HashToken):
                name_inheritance_out.append(f"#{token.value}")
                continue

            # Is a bear ident (such as img)
            if isinstance(token, tokenizer.IdentToken):
                name_inheritance_out.append(token.value)
                continue

            raise Exception("Unhandled token encountered")

        if len(name_inheritance_out) == 0:
            raise Exception("No names found in prelude")

        if len(name_inheritance_out) == 1:
            name_out = name_inheritance_out[0]
            if name_out in self.sizing_rules:
                named_sizing_rule = self.sizing_rules[name_out]
                if named_sizing_rule.sizing_rule is not None:
                    raise Exception("Conflicting size information")
                named_sizing_rule.sizing_rule = sizing_rule
                return
            named_sizing_rule = NamedSizingRule(name=name_inheritance_out[0], sizing_rule=sizing_rule)
            self.sizing_rules[named_sizing_rule.name] = named_sizing_rule
            return

        if len(name_inheritance_out) == 2:
            base_name = name_inheritance_out[1]
            if base_name in self.sizing_rules:
                base_named_sizing_rule = self.sizing_rules[base_name]
            else:
                base_named_sizing_rule = NamedSizingRule(name=base_name, sizing_rule=None)
                self.sizing_rules[base_name] = base_named_sizing_rule
            named_sizing_rule = NamedSizingRule(name=name_inheritance_out[0], sizing_rule=sizing_rule)
            base_named_sizing_rule.store_parent(named_sizing_rule)
            return

        raise Exception("More then 2 levels of name inheritance found!")
