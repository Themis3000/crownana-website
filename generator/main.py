from jinja2 import Environment, FileSystemLoader, select_autoescape
import yaml
env = Environment(
    loader=FileSystemLoader("../templates"),
    autoescape=select_autoescape()
)


# Generate gallery documents
template = env.get_template("gallery.jinja2")
gallery_config = yaml.safe_load(open("../gallery_config.yml"))
all_entries = []

for category_name in gallery_config:
    category = gallery_config[category_name]
    all_entries.extend(category)
    category_content = template.render(img_entries=category, selected=category_name)
    with open(f"../public/gallery/{category_name}.html", "w") as f:
        f.write(category_content)

all_content = template.render(img_entries=all_entries, selected="all")
with open("../public/gallery/index.html", "w") as f:
    f.write(all_content)
