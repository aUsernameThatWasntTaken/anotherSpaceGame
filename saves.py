import json

def load(fileName, default):
    try:
        with open(fileName) as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default