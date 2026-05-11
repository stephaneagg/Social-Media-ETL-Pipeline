import json

def extract(path):
    with open(path) as f:
        return json.load(f)