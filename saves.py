import json
from asyncio import Queue


defaultSave = {
    "money":1_000_000,
    "infrastructure":{
        "earth":[
            {"type":"VAB", "level":1},
            {"type":"launchPad","level":1}
            ]
    }
}

class World:
    def __init__(self, jsonDict):
        self.money = int(jsonDict["money"]) # casting value for myPy to accept typing
        # this can be used later if changes are needed to structure handling
        # self.infrastructure = dict([(body, [structure for structure in structures]) for body,structures in jsonDict["infrastructure"].items()])
        self.infrastructure = jsonDict["infrastructure"]
        self.vABSpeed = sum([item["level"] for item in self.infrastructure["earth"] if item["type"]=="VAB"])
        # in seconds with one Lvl1 VAB:
        self.rocketBuildTime = 10
        self.rocketCost = 1000
        self.rocketBuildQueue = Queue()
        self.rocketLaunchQueue = Queue()
    
    def buildRocket(self):
        self.rocketBuildQueue.put("rocket")
        self.money -= self.rocketCost

def getWorld(saveFileName):
    if saveFileName == "None":
        return World(defaultSave)
    else:
        try:
            with open(saveFileName+".json") as f:
                return World(json.load(f))
        except json.JSONDecodeError:
            print("Save File corrupted or incompatible, starting new save")
            return World(defaultSave)
