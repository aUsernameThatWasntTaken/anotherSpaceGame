import json
from BackendCode.WorldClass import World


defaultSave = {
    "money":1_000_000,
    "infrastructure":{
        "VAB":1,
        "Launchpads":1
    },
    "unlocks":{"rocketSize":0},
    "events":[]
}

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

def saveGame(world: World, saveFileName):
    with open(saveFileName+".json") as f:
        json.dump(world.toDict(), f, indent=4)