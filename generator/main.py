"""
Handles generating the site content for deployment.
Cutting-edge BLAZINGLY FAST static site generation tool (fire emojis)

Please don't make judgements about my programming skills based on this.
Most of this was written in little gaps of time on my 2008 laptop without an internet connection.
I could roast a lot of what I've written here.
"""
from pathlib import Path
import bs4
import yaml
from glob import glob
from themis_md import ThemisMDDoc
from utils import BlogPost, env
from typing import List, Dict
from html import escape
from bs4 import BeautifulSoup
from css import CSSSizingParser, SizingRule
from PIL import Image
import urllib.parse
import shutil

SRC_PATH = Path("../public")
OUT_PATH = Path("../out")

# TODO these get path functions in GenFile and ImageEntry are 100% real scuffed. Check out Path.as_posix and see if it's
# a good replacement. If not, at least make a single helper function instead of reimplementing the same business
# logic in multiple places.


class GenFile:
    def __init__(self, path: Path):
        self.path = path
        self.processed = False
        self.out_path = OUT_PATH.joinpath(*path.parts[2:])
        self.out_path.parent.mkdir(parents=True, exist_ok=True)

    def update_out_ext(self, suffix: str):
        self.out_path = self.out_path.with_suffix(suffix)

    def read_src_str(self) -> str:
        with open(self.path, "r") as f:
            return f.read()

    def write_out_str(self, data: str):
        with open(self.out_path, "w") as f:
            f.write(data)

    def mark_processed(self):
        if self.processed:
            raise Exception("GenFile was double marked as processed!")
        self.processed = True

    def get_url_path(self) -> str:
        return "/".join([*self.out_path.parts[2:]])


class ImageEntry:
    def __init__(self, path: str | Path, sizing_rule: SizingRule, scale_modifier=1.25):
        if not isinstance(path, Path):
            path = Path(path)
        self.path = path
        self.sizing_rule = sizing_rule
        self.scale_modifier = scale_modifier
        self.needs_rescaling = self._get_needs_rescaling()
        out_file_name = f"thumb_{sizing_rule.widthPx}_{sizing_rule.heightPx}_{scale_modifier}x_{path.parts[-1]}"
        out_path_dir = OUT_PATH.joinpath(*path.parts[2:-1])
        self.out_path = out_path_dir.joinpath(out_file_name)

    def _get_needs_rescaling(self) -> bool:
        image = Image.open(self.path)
        needs_rescaling = False
        if self.sizing_rule.widthPx is not None:
            if image.width > self.sizing_rule.widthPx:
                needs_rescaling = True
        if self.sizing_rule.heightPx is not None:
            if image.height > self.sizing_rule.heightPx:
                needs_rescaling = True
        return needs_rescaling

    def get_out_url(self) -> str:
        parts = list(self.out_path.parts)[2:]
        return "/" + "/".join(parts)

    def convert(self):
        if not self.needs_rescaling:
            raise Exception("Convert was called, but no rescaling is needed!")

        if self.check_completed():
            return

        image = Image.open(self.path)
        height_size = self.sizing_rule.heightPx
        if height_size is None:
            height_size = image.height
        width_size = self.sizing_rule.widthPx
        if width_size is None:
            width_size = image.width
        image.thumbnail((int(width_size * self.scale_modifier), int(height_size * self.scale_modifier)))
        image.save(self.out_path)

    def get_unique(self) -> str:
        return f"{self.path.as_posix()}_{self.sizing_rule.widthPx}_{self.sizing_rule.heightPx}_{self.scale_modifier}"

    def check_completed(self) -> bool:
        return self.out_path.exists()


class SiteGenerator:
    def __init__(self):
        file_strings = glob(f"{str(SRC_PATH)}/**", recursive=True, include_hidden=True)
        self.file_paths: List[GenFile] = []
        for file_string in file_strings:
            file_path = Path(file_string)
            if file_path.is_dir():
                continue
            self.file_paths.append(GenFile(file_path))

        self.blog_entries: List[BlogPost] = []
        with open("../public/resources/styles.css", "r") as f:
            self.css_sizing = CSSSizingParser()
            self.css_sizing.add_stylesheet(f.read())
        self.img_mappings: Dict[str, ImageEntry] = {}

    def add_img_mapping(self, img_entry: ImageEntry):
        unique = img_entry.get_unique()
        if unique in self.img_mappings:
            return
        self.img_mappings[unique] = img_entry

    def pre_actions(self):
        self.generate_gallery_documents()
        self.process_tmd()
        self.generate_blog_home()
        self.generate_rss_feed()

    def run_generation(self):
        self.pre_actions()

        for gen_file in self.get_unprocessed_file_type([".html"]):
            self.process_html(gen_file)

        for img_mapping in self.img_mappings.values():
            img_mapping.convert()

        for gen_file in self.file_paths:
            if not gen_file.processed:
                self.process_file(gen_file)

    def process_html(self, gen_file: GenFile):
        soup = BeautifulSoup(gen_file.read_src_str(), features="html.parser")
        img_tags = soup.find_all(name="img")
        for img in img_tags:
            if not isinstance(img, bs4.Tag):
                raise Exception("Image tag... Wasn't a Tag?")
            if "no-thumb" in img.get("class", ""):
                continue
            size_rule = self.css_sizing.get_tag_size(img)
            if size_rule is None:
                continue
            classes = img.get("class", "")
            rel_src_string = urllib.parse.unquote(img["src"])
            if rel_src_string.startswith("/"):
                rel_src_string = rel_src_string[1:]
            over_scale = 1.25
            if "no-over-scale" in classes:
                over_scale = 1
            img_entry = ImageEntry(path=SRC_PATH.joinpath(rel_src_string), sizing_rule=size_rule, scale_modifier=over_scale)
            if not img_entry.needs_rescaling:
                continue
            self.add_img_mapping(img_entry)
            if "no-a" not in classes:
                a_element = soup.new_tag("a", href=img["src"])
                img.wrap(a_element)
            img["src"] = img_entry.get_out_url()
        gen_file.write_out_str(soup.prettify(formatter=bs4.Formatter(indent=4)))
        gen_file.mark_processed()

    @staticmethod
    def process_file(gen_file: GenFile):
        shutil.copyfile(src=gen_file.path, dst=gen_file.out_path)
        gen_file.mark_processed()

    def get_unprocessed_file_type(self, file_types: List[str]):
        for gen_file in self.file_paths:
            if gen_file.path.suffix in file_types and not gen_file.processed:
                yield gen_file

    def generate_gallery_documents(self):
        gallery_template = env.get_template("gallery.jinja2")
        gallery_config = yaml.safe_load(open("../gallery_config.yml"))

        categories = {"all": gallery_config["images"]}
        categories_info = [{"name": "all", "href": f"/gallery/all.html"}]
        for entry in gallery_config["images"]:
            category = entry["category"]
            if category not in categories:
                categories[category] = []
                categories_info.append({"name": category, "href": f"/gallery/{category}.html"})
            categories[category].append(entry)

        for category_name, category in categories.items():
            category_content = gallery_template.render(img_entries=category, categories_info=categories_info,
                                                       selected_category=category_name)
            out_file = OUT_PATH.joinpath(f"gallery/{category_name}.html")
            gen_file = GenFile(path=out_file)
            gen_file.write_out_str(category_content)
            self.file_paths.append(gen_file)

    def process_tmd(self):
        for gen_file in self.get_unprocessed_file_type([".tmd"]):
            doc = ThemisMDDoc(open(gen_file.path, "r"))
            gen_file.update_out_ext(".html")
            gen_file.write_out_str(doc.gen_html())

            if doc.meta.get("type") == "blog-post":
                self.blog_entries.append(BlogPost(
                    entry_style=doc.meta["entry_style"],
                    title=doc.meta["title"],
                    teaser=doc.meta["teaser"],
                    date=doc.meta["date"],
                    path=gen_file.out_path,
                    entry_meta=doc.meta.get("entry_meta")
                ))

            gen_file.mark_processed()
            output_gen_file = GenFile(gen_file.out_path)
            self.file_paths.append(output_gen_file)

    def generate_blog_home(self):
        blog_template = env.get_template("blog.jinja2")
        self.blog_entries.sort(reverse=True, key=lambda x: x.get_timestamp())
        blog_content = blog_template.render(blog_entries=self.blog_entries)
        gen_file = GenFile(OUT_PATH.joinpath("blog/index.html"))
        gen_file.write_out_str(blog_content)
        self.file_paths.append(gen_file)

    def generate_rss_feed(self):
        rss_path = OUT_PATH.joinpath("blog/rss.xml")
        rss_f = open(rss_path, "w")
        rss_f.write("""<?xml version="1.0" encoding="UTF-8" ?>
        <rss version="2.0">
        <channel>
            <title>Crownanabread Blog</title>
            <link>https://crownanabread.com</link>
            <description>The crownanabread personal blog</description>
        """)
        for entry in self.blog_entries:
            full_url = escape(f"https://crownanabread.com/{'/'.join([*entry.path.parts[2:]])}")
            rss_f.write(f"""
                <item>
                    <title>{escape(entry.title)}</title>
                    <link>{full_url}</link>
                    <description>{escape(entry.teaser)} - view the full blog post at {full_url}</description>
                    <pubDate>{entry.get_rfc822()}</pubDate>
                </item>
            """)
        rss_f.write("""
        </channel>
        </rss>
        """)


if __name__ == "__main__":
    SiteGenerator().run_generation()
