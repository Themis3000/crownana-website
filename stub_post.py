from datetime import datetime

post_name = input("Enter post name: ")
teaser = input("Enter teaser: ")

now = datetime.now()
time_file_name = f"{now.month}.{now.day}.{now.year-2000}_{post_name.replace(' ', '_')}.tmd"
time_standard = f"{now.month}/{now.day}/{now.year-2000}"
date_meta = f"{{\"month\": \"{now.strftime('%B')}\", \"day\": \"{now.day}\", \"year\": \"{now.year}\"}}"

output = f"""----
title: {time_standard} {post_name}
teaser: {teaser}
style: default
type: blog-post
entry_style: micro-cal
entry_meta: {date_meta}
date: {time_standard}
----
# {time_standard} {post_name}
"""

with open(f"./public/blog/posts/{time_file_name}", "w") as f:
    f.write(output)
