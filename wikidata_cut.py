from pymongo import MongoClient
from joblib import Parallel, delayed
import json

types_file = "wikidata_types.json"
wikidata_in = "wikidata"
wikidata_out="wikidata_cut"

client = MongoClient()
col_in = client[wikidata_in]["data"]
col_out = client[wikidata_out]["data"]


col_in.create_index("id")
col_in.create_index("claims.P31.mainsnak.datavalue.value.id")

with open(types_file) as f:
    kahi_wdata_ids = json.loads(f.read())

print(f"readed {types_file} with types len = {len(kahi_wdata_ids)}")

def process_one(t):
    cursor=col_in.find({"claims.P31.mainsnak.datavalue.value.id":t})
    for i in cursor:
        try:
            col_out.insert_one(i)
        except Exception as e: # Duplicate key could happend and it is normal
            pass               # it is because one record can be part of different types 
                               # and then and interception can happen. 
            

backend = 'multiprocessing'
out = Parallel(n_jobs=20, backend=backend,verbose=10)(delayed(process_one)(t) for t in kahi_wdata_ids)