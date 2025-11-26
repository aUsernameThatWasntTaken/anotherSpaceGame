import json

def load(fileName, default):
    with open(fileName) as f:
        return json.load(f)