from typing import TextIO
from .element_base import TElement, TMergeableElement
from abc import ABC, abstractmethod
import re
import html


class TSimpleTextTag(TElement, ABC):
    # noinspection PyPropertyDefinition
    @staticmethod
    @property
    @abstractmethod
    def tag_name() -> str:
        pass

    def gen_html(self) -> str:
        text = html.escape(self.content.rstrip())
        return f"<{self.tag_name}>{text}</{self.tag_name}>"


class TParagraph(TMergeableElement):
    keyword = ""
    re_a_tag = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")
    re_i_tag = re.compile(r"\*([^*]+)\*")
    re_b_tag = re.compile(r"\*\*([^*]+)\*\*")

    def gen_html(self) -> str:
        cleaned_content = [html.escape(content) for content in self.content_list]
        content_str = "<br>\n".join(cleaned_content)

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
        alt_text = html.escape(match.group(1))
        src = html.escape(match.group(2))
        return f"<img src='{src}' alt='{alt_text}'>"


class TBulletPoint(TMergeableElement):
    @classmethod
    def is_element(cls, fragment: str) -> bool:
        stripped = fragment.rstrip()
        return stripped.startswith("- ")

    def gen_html(self) -> str:
        depth_list = []
        depth_step = 4
        for content in self.content_list:
            before_length = len(content)
            content = content.lstrip()
            leading_spaces = len(content) - before_length
            depth = leading_spaces // depth_step
            depth_list.append({"content": content, "depth": depth})

        out_str = ""
        current_depth = 0
        for line in depth_list:
            pass

        return out_str


# The list of element types available for keyword based use
elements_types = [THeader, THeader2, THeader3, THeader4, TImage, TBulletPoint]
