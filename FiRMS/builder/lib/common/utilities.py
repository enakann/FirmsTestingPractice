import os
import json
from settings import QUERIES_PATH,CONFIG_PATH

def writetofile(filename,data):
    with open(filename, "w") as fl:
        fl.write(data.encode("utf-8"))
        fl.close()

def load_queries(module):
    query_fl = os.path.join(QUERIES_PATH, '{}.json'.format(module))
    try:
        with open(query_fl, 'r') as f:
            data = json.load(f)

    except:
        raise Exception("Failed to load query file {}".format(query_fl))
    return data

