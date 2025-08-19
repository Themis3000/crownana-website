import re


class ReReplacer:
    def __init__(self, re_statement: str, template_str: str):
        self.re = re.compile(re_statement)
        self.template = template_str

    def _custom_sub(self, match: re.Match[str]) -> str:
        groups = match.groups()
        output = self.template
        for i, group_match in enumerate(groups):
            output = output.replace(f"|${i}", group_match)
        return output

    def do_subs(self, str_content: str) -> str:
        return self.re.sub(self._custom_sub, str_content)
