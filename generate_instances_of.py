from pymongo import MongoClient
import json

kahi_db = "kahi_dev"
wikidata_db = "wikidata"
scholarly_article_id = "Q13442814" ## pares are not required and they are a lot, about 37 million
output_file="wikidata_types.json" ##instances of

omit_ids = [{'id': 'Q13442814', 'label': 'scholarly article', 'count': 37450016}]

client =  MongoClient()
db = client[wikidata_db]
col_in = db["data"]

print("creating required indexes in wikidata")
col_in.create_index("id")
col_in.create_index("claims.P31.mainsnak.datavalue.value.id")

print(f"Getting wikidata ids for {kahi_db} affiliations")
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


kahi_wdata_ids=list(set(kahi_wdata_ids))
len(kahi_wdata_ids)

affiliations = []
for i in kahi_wdata_ids:
    value = col_in.find_one({"id":i},{"_id":0})
    affiliations.append(value)

print("Getting types")
instances_types=[]
for i in affiliations:
    if i == None:
        continue
    if "claims" in i.keys():
        if "P31" in i["claims"].keys():
            for j in i["claims"]["P31"]:
                instances_types.append(j["mainsnak"]["datavalue"]["value"]["id"])

instances_types = list(set(instances_types))
len(instances_types)

for o in omit_ids:
    if o["id"] in instances_types:
        instances_types.remove(o["id"])

print(f"found {len(instances_types)} types")
with open(output_file,"w") as f:
    f.write(json.dumps(instances_types))