import json

class World:
    def __init__(self, jsonDict):
        self.money = int(jsonDict["money"]) # casting value for myPy to accept typing
        # this can be used later if changes are needed to structure handling
        # self.infrastructure = dict([(body, [structure for structure in structures]) for body,structures in jsonDict["infrastructure"].items()])
        self.infrastructure = jsonDict["infrastructure"]
        self.vABSpeed = sum([item["level"] for item in self.infrastructure["earth"] if item["type"]=="VAB"])

def load(fileName):
    with open(fileName) as f:
        return json.load(f)