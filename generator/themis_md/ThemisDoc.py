from .element_base import TElement
from .elements import elements_types, TParagraph
from typing import List, TextIO
import re


class ThemisMDDoc:
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
            metadata[meta_name] = meta_value
        return metadata

    def gen_html(self) -> str:
        out = ""
        for element in self.element_list:
            out += element.gen_html() + "\n"
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

            # Special case for paragraphs
            # If both the last and current element is a <p>, they should be merged into one longer multiline <p>
            if len(elements) > 0:
                last_element = elements[-1]
                if isinstance(element, TParagraph) and isinstance(last_element, TParagraph):
                    last_element.merge_paragraph(element)
                    continue

            elements.append(element)

        return elements

    @staticmethod
    def _parse_element(search: str, f: TextIO) -> TElement:
        for element_type in elements_types:
            if search.startswith(element_type.keyword):
                return element_type(f)

        return TParagraph(f)
