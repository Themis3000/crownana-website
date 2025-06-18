from typing import TextIO
from .element_base import TElement
from abc import ABC, abstractmethod


class TSimpleTextTag(TElement, ABC):
    # noinspection PyPropertyDefinition
    @staticmethod
    @property
    @abstractmethod
    def tag_name() -> str:
        pass

    def gen_html(self) -> str:
        return f"<{self.tag_name}>{self.content.rstrip()}</{self.tag_name}>"

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


class THeader(TSimpleTextTag):
    keyword = "# "
    tag_name = "h1"


class THeader2(TSimpleTextTag):
    keyword = "## "
    tag_name = "h2"


class THeader3(TSimpleTextTag):
    keyword = "### "
    tag_name = "h3"


class THeader4(TSimpleTextTag):
    keyword = "#### "
    tag_name = "h4"


# The list of element types available for keyword based use
elements_types = [THeader, THeader2, THeader3, THeader4]
