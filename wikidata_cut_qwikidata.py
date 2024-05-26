import sys
import time
import json
try:
    from qwikidata.entity import WikidataItem
    from qwikidata.json_dump import WikidataJsonDump
    from qwikidata.utils import dump_entities_to_json
    from pymongo import MongoClient
    from pymongo.errors import DuplicateKeyError
except:
    print("install qwikidata and pymongo package with: pip install qwikidata pymongo")
    sys.exit(1)

types_file = "wikidata_types.json"
wjd_dump_path = "/storage/wikidata/wikidata-20220103-all.json.gz" #wikidata compressed file
wikidata_db="wikidata_cut"

client = MongoClient()
col = client[wikidata_db]["data"]

print("this process can take about 9 hours")
# create an instance of WikidataJsonDump
wjd = WikidataJsonDump(wjd_dump_path)

with open(types_file) as f:
    kahi_wdata_ids = json.loads(f.read())

print(f"readed {types_file} with types len = {len(kahi_wdata_ids)}")
init= time.time()
for ii, entity_dict in enumerate(wjd):
    if ii%10000 == 0:
        print(ii) 
    if "P31" in entity_dict["claims"].keys():
        for j in entity_dict["claims"]["P31"]:
            if "datavalue" in j["mainsnak"].keys():
                if j["mainsnak"]["datavalue"]["value"]["id"] in kahi_wdata_ids:
                    try:
                        col.insert_one(entity_dict)
                    except DuplicateKeyError:
                        print(f"doublicate Key with rec {entity_dict['id']}")
                        pass
end= time.time()
t = (end-init)/60
print("Execution time = {t} mins ")
