import dataclasses


@dataclasses.dataclass()
class BlogPost:
    title: str
    teaser: str
    color_theme: str
    date: str
    path: str
