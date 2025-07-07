import json
from .element_base import TElement
from .elements import elements_types, TParagraph, TMergeableElement
from typing import List, TextIO
import re
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os

module_dir = os.path.dirname(__file__)
env = Environment(
    loader=FileSystemLoader(os.path.join(module_dir, "styles")),
    autoescape=select_autoescape()
)


class ThemisMDDoc:
    """
    Parses a document and holds it in memory. Then, can convert said document into usable html.

    Yes, I know this was implemented in a really silly way and there's better ways. It was just more fun this way :)
    """
    max_symbol_size = 10
    re_value = re.compile(r"^([^ ]+): ?(.+)$")

    def __init__(self, f: TextIO):
        if f.read(5) == "----\n":
            self.meta = self._read_meta(f)
        else:
            self.meta = {}
            f.seek(0)

        self.element_list = self._parse_elements(f)

    def _read_meta(self, f: TextIO) -> dict:
        metadata = {}
        while (line := f.readline()) != "----\n":
            match = self.re_value.match(line)
            assert match is not None, "Invalid metadata!"
            meta_name = match.group(1)
            meta_value = match.group(2)
            if meta_value.startswith("{"):
                meta_value = json.loads(meta_value)
            metadata[meta_name] = meta_value
        return metadata

    def gen_html(self) -> str:
        out = ""
        for element in self.element_list:
            out += element.gen_html()

        style = self.meta.get("style")
        if not style:
            return out

        template = env.get_template(f"{style}.jinja2")
        out = template.render(content_html=out, **self.meta)
        return out

    def _parse_elements(self, f: TextIO) -> List[TElement]:
        elements = []
        while True:
            start_pos = f.tell()
            search = f.read(self.max_symbol_size)
            if len(search) == 0:
                break
            f.seek(start_pos)

            element = self._parse_element(search, f)

            # If the currently parsed element is mergeable and the last is of the same type, merge them instead.
            current_type = type(element)
            if issubclass(current_type, TMergeableElement) and len(elements) > 0:
                last_element = elements[-1]
                if isinstance(last_element, current_type):
                    last_element.merge(element)
                    continue

            elements.append(element)

        return elements

    @staticmethod
    def _parse_element(search: str, f: TextIO) -> TElement:
        for element_type in elements_types:
            if element_type.is_element(search):
                return element_type(f)

        return TParagraph(f)
