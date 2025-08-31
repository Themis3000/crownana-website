import dataclasses
import os
from pathlib import Path

from PIL import Image
import yaml
from glob import glob
from themis_md import ThemisMDDoc
from utils import BlogPost, env
from typing import List
from html import escape


@dataclasses.dataclass()
class GenFile:
    path: Path
    do_relocation: bool = True
    processed: bool = False


class SiteGenerator:
    def __init__(self):
        self.src_dir = "../public"
        self.out_dir = "../out"
        if not os.path.exists(self.out_dir):
            os.mkdir(self.out_dir)

        file_strings = glob(f"{self.src_dir}/**", recursive=True)
        self.file_paths: List[GenFile] = []
        for file_string in file_strings:
            file_path = Path(file_string)
            if file_path.is_dir():
                continue
            gen_file = GenFile(path=file_path)
            self.file_paths.append(gen_file)

        self.blog_entries: List[BlogPost] = []

    def pre_actions(self):
        self.generate_gallery_documents()

    def run_generation(self):
        pass

    def process_file(self, file_path: Path):
        pass

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
            out_file = Path(f"{self.out_dir}/gallery/{category_name}.html")
            with open(out_file, "w") as f:
                f.write(category_content)
            self.file_paths.append(GenFile(path=out_file, do_relocation=False))


if __name__ == "__main__":
    SiteGenerator().run_generation()
quit()


# Convert tmd files to html pages, and collect blog post info
blog_entries: List[BlogPost] = []
tmd_files = glob("../public/**/*.tmd", recursive=True)
for tmd_file in tmd_files:
    with open(tmd_file, "r") as f:
        doc = ThemisMDDoc(f)
    new_path = tmd_file[:-3] + "html"
    with open(new_path, "w") as f:
        f.write(doc.gen_html())
    # collect blog post info, if available
    if doc.meta.get("type") == "blog-post":
        blog_entries.append(BlogPost(
            entry_style=doc.meta["entry_style"],
            title=doc.meta["title"],
            teaser=doc.meta["teaser"],
            color_theme=doc.meta["color_theme"],
            date=doc.meta["date"],
            path=new_path[9:],
            entry_meta=doc.meta.get("entry_meta")
        ))


# generate blog post home page
blog_template = env.get_template("blog.jinja2")
blog_entries.sort(reverse=True, key=lambda x: x.get_timestamp())
blog_content = blog_template.render(blog_entries=blog_entries)
with open(f"../public/blog/index.html", "w") as f:
    f.write(blog_content)


# generate rss feed
rss_f = open("../public/blog/rss.xml", "w")
rss_f.write("""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
    <title>Crownanabread Blog</title>
    <link>https://crownanabread.com</link>
    <description>The crownanabread personal blog</description>
""")
for entry in blog_entries:
    clean_path = os.path.normpath(entry.path)
    split_path = clean_path.split(os.sep)
    relative_path = "/".join(split_path)
    full_url = escape(f"https://crownanabread.com{relative_path}")
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
