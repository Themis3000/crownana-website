from typing import TextIO
from .element_base import TElement


class THeader(TElement):
    keyword = "# "

    def gen_html(self):
        return f"<h1>{self.content.rstrip()}</h1>"

    def _read_content(self, f: TextIO) -> str:
        return f.readline()


class TParagraph(TElement):
    keyword = ""

    def _read_content(self, f: TextIO) -> str:
        return f.readline()

    def gen_html(self) -> str:
        return f"<p>{self.content.rstrip()}</p>"


# The list of element types available for use, besides paragraph
elements_types = [THeader]
