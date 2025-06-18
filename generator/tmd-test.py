from themis_md import ThemisMDDoc

f = open("test.tmd", "r")
doc = ThemisMDDoc(f)
print(doc.gen_html())
