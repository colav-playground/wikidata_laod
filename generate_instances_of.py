from pymongo import MongoClient
import json

kahi_db = "kahi_dev"
scholarly_article_id = "Q13442814" ## pares are not required and they are a lot, about 37 million
output_file="wikidata_types.json" ##instances of


client =  MongoClient()

#busco los ids de los que ya tengo para sacar los tipos de institución y luego hacer el corte
kahi_wdata_cursor = client[kahi_db]["affiliations"].find({"external_ids.source":"wikidata"},{"_id":0,"external_ids":1})
kahi_wdata_ids=[]
for i in kahi_wdata_cursor:
    for j in i["external_ids"]:
        if j["source"] == "wikidata":
            kahi_wdata_ids.append(j["id"])
            break
if scholarly_article_id in kahi_wdata_ids:
    kahi_wdata_ids.remove(scholarly_article_id)

print(f"found {len(kahi_wdata_ids)} types")
with open(output_file,"w") as f:
    f.write(json.dumps(kahi_wdata_ids))