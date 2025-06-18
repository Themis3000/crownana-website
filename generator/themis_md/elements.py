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

    def __init__(self, f: TextIO):
        super().__init__(f)
        self.content_list = [self.content.rstrip()]

    def _read_content(self, f: TextIO) -> str:
        return f.readline()

    def gen_html(self) -> str:
        content_with_breaks = "<br>\n".join(self.content_list)
        return f"<p>{content_with_breaks}</p>"

    def merge_paragraph(self, other):
        self.content_list.extend(other.content_list)


# The list of element types available for use, besides paragraph
elements_types = [THeader]
