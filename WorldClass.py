from asyncio import Queue

class World:
    def __init__(self, jsonDict):
        self.money = int(jsonDict["money"]) # casting value for myPy to accept typing
        self.vABlevel = jsonDict["infrastructure"]["VAB"]
        self.pads = jsonDict["infrastructure"]["Launchpads"]
        self.rocketsLaunched = jsonDict["rocketsLaunched"]
    
    def buildRocket(self):
        self.rocketBuildQueue.put("rocket")
        self.money -= self.rocketCost
