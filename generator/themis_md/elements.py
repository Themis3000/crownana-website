from typing import TextIO
from .element_base import TElement
from abc import ABC, abstractmethod
import re


class TSimpleTextTag(TElement, ABC):
    # noinspection PyPropertyDefinition
    @staticmethod
    @property
    @abstractmethod
    def tag_name() -> str:
        pass

    def gen_html(self) -> str:
        return f"<{self.tag_name}>{self.content.rstrip()}</{self.tag_name}>"


class TParagraph(TElement):
    keyword = ""
    re_a_tag = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")
    re_i_tag = re.compile(r"\*([^*]+)\*")
    re_b_tag = re.compile(r"\*\*([^*]+)\*\*")

    def __init__(self, f: TextIO):
        super().__init__(f)
        self.content_list = [self.content.rstrip()]

    def gen_html(self) -> str:
        content_str = "<br>\n".join(self.content_list)

        def a_sub(match):
            text = match.group(1)
            link = match.group(2)
            return f"<a href='{link}'>{text}</a>"
        content_str = self.re_a_tag.sub(a_sub, content_str)

        def b_sub(match):
            return f"<b>{match.group(1)}</b>"
        content_str = self.re_b_tag.sub(b_sub, content_str)

        def i_sub(match):
            return f"<i>{match.group(1)}</i>"
        content_str = self.re_i_tag.sub(i_sub, content_str)

        return f"<p>{content_str}</p>"

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


class TImage(TElement):
    keyword = "!["
    re_img_tag = re.compile(r"^(.*)\]\((.*)\)$")

    def gen_html(self) -> str:
        match = self.re_img_tag.match(self.content)
        assert match is not None, "Improper image line element!"
        alt_text = match.group(1)
        src = match.group(2)
        return f"<img src='{src}' alt='{alt_text}'>"


# The list of element types available for keyword based use
elements_types = [THeader, THeader2, THeader3, THeader4, TImage]
