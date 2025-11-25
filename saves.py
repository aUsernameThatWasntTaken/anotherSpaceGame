import json

def load(fileName, default):
    with open(fileName) as f:
        try:
            saveJson = json.load(f)
        except json.JSONDecodeError:
            return default
        return saveJson