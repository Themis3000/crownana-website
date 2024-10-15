from jinja2 import Environment, FileSystemLoader, select_autoescape
import yaml
env = Environment(
    loader=FileSystemLoader("../templates"),
    autoescape=select_autoescape()
)


# Generate gallery documents
template = env.get_template("gallery.jinja2")
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
    category_content = template.render(img_entries=category, categories_info=categories_info,
                                       selected_category=category_name)
    with open(f"../public/gallery/{category_name}.html", "w") as f:
        f.write(category_content)
