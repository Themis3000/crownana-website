import os
from PIL import Image
from jinja2 import Environment, FileSystemLoader, select_autoescape
import yaml
from glob import glob
from themis_md import ThemisMDDoc


env = Environment(
    loader=FileSystemLoader("../templates"),
    autoescape=select_autoescape()
)


# Generate gallery documents
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
    if not os.path.exists(f"../public/resources/gallery/thumbs/{entry['path']}"):
        with Image.open(f"../public/resources/gallery/{entry['path']}") as img:
            img.thumbnail((1024, 1024))
            img.save(f"../public/resources/gallery/thumbs/{entry['path']}")


for category_name, category in categories.items():
    category_content = gallery_template.render(img_entries=category, categories_info=categories_info,
                                               selected_category=category_name)
    with open(f"../public/gallery/{category_name}.html", "w") as f:
        f.write(category_content)


# Generate blog home page
blog_template = env.get_template("blog.jinja2")
blog_config = yaml.safe_load(open("../blog_config.yml"))

blog_content = blog_template.render(blog_entries=blog_config["posts"])
with open(f"../public/blog/index.html", "w") as f:
    f.write(blog_content)


# Convert tmd files to html pages
tmd_files = glob("../public/**/*.tmd", recursive=True)
for tmd_file in tmd_files:
    with open(tmd_file, "r") as f:
        doc = ThemisMDDoc(f)
    new_path = tmd_file[:-3] + "html"
    with open(new_path, "w") as f:
        f.write(doc.gen_html())
