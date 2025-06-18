from .element_base import TElement
from .elements import elements_types, TParagraph
from typing import List, TextIO


class ThemisMDDoc:
    max_symbol_size = 10

    def __init__(self, f: TextIO):
        self.element_list = self._parse_elements(f)

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
