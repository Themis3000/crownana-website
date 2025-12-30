from .element_base import TElement, TMergeableElement
from abc import ABC, abstractmethod
import re
import html
from .utils import ReReplacer


class TParagraph(TMergeableElement):
    a_tag_replacer = ReReplacer(r"\[([^\]]*)\]\(([^)]*)\)", "<a href='$2'>$1</a>")
    i_tag_replacer = ReReplacer(r"\*([^*]+)\*", "<i>$1</i>")
    b_tag_replacer = ReReplacer(r"\*\*([^*]+)\*\*", "<b>$1</b>")
    code_tag_replacer = ReReplacer("`([^`]+)`", "<code>$1</code>")
    replacers = [a_tag_replacer, b_tag_replacer, i_tag_replacer, code_tag_replacer]

    @classmethod
    def _replace_tags(cls, str_content: str) -> str:
        out = str_content
        for replacer in cls.replacers:
            out = replacer.do_subs(out)
        return out

    def gen_html(self) -> str:
        cleaned_content = [html.escape(content.strip()) for content in self.content_list]
        content_str = "<br>".join(cleaned_content) + "<br>"
        content_str = self._replace_tags(content_str)
        return f"<p>{content_str}</p>"


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
        stripped = fragment.lstrip(" ")
        return stripped.startswith("- ")

    def gen_html(self) -> str:
        depth_list = []
        depth_step = 4
        for content in self.content_list:
            before_length = len(content)
            content = content.strip()
            content = content[2:]
            leading_spaces = before_length - len(content)
            depth = leading_spaces // depth_step
            depth_list.append({"content": content, "depth": depth})

        out_str = "<ul>"
        current_depth = 0
        for line in depth_list:
            if line["depth"] > current_depth:
                out_str += f"<ul>"
            elif current_depth > line["depth"]:
                out_str += "</ul></li>"
            elif len(out_str) > 5:
                out_str += "</li>"
            out_str += "<li>"
            out_str += line["content"]
            current_depth = line["depth"]
        out_str += "</li></ul>"
        return out_str


class TSectionDivider(TElement):
    keyword = "____"

    def gen_html(self) -> str:
        return "<hr>"


# The list of element types available for keyword based use
elements_types = [THeader, THeader2, THeader3, THeader4, TImage, TBulletPoint, TSectionDivider]
