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
template_content = template.render(img_entries=all_entries, selected="all")
with open("../public/pages/gallery/home.html", "w") as f:
    f.write(template_content)
