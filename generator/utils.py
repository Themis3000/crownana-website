import dataclasses
import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
import glob
import os
from email.utils import format_datetime

env = Environment(
    loader=FileSystemLoader("../templates"),
    autoescape=select_autoescape()
)

blog_entry_style_paths = glob.glob("../templates/blog_entry_styles/*.jinja2")
blog_entry_styles = {}
for blog_entry_style_path in blog_entry_style_paths:
    file_name = os.path.basename(blog_entry_style_path)
    name = file_name[:-7]
    template = env.get_template(f"/blog_entry_styles/{file_name}")
    blog_entry_styles[name] = template


@dataclasses.dataclass()
class BlogPost:
    entry_style: str
    title: str
    teaser: str
    color_theme: str
    date: str
    path: Path
    entry_meta: dict | None

    timezone = datetime.timezone(datetime.timedelta(hours=-6))

    def get_url_path(self) -> str:
        stripped_leading = Path(*self.path.parts[2:])
        return "/" + stripped_leading.as_posix()

    def get_timestamp(self):
        return datetime.datetime.strptime(self.date, "%m/%d/%y").timestamp()

    def get_rfc822(self):
        date = datetime.datetime.strptime(self.date, "%m/%d/%y").astimezone(self.timezone)
        return format_datetime(date)

    def render_entry(self):
        assert self.entry_style in blog_entry_styles, "Blog entry style does not exist!"
        entry_template = blog_entry_styles[self.entry_style]
        return entry_template.render(blog_entry=self)
