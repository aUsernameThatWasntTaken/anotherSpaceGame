import asyncio

class World:
    def __init__(self, jsonDict):
        self.rocketBuildTime = 10 # seconds with a Lvl1 VAB
        self.rocketCost = 1000
        self.rocketBuildQueue = asyncio.Queue()
        self.rocketLaunchQueue = asyncio.Queue()
        self.payloadQueue = asyncio.Queue()
    
    def readWorldData(self, jsonDict):
        self.money = int(jsonDict["money"]) # casting value for myPy to accept typing
        self.vABlevel = jsonDict["infrastructure"]["VAB"]
        self.pads = jsonDict["infrastructure"]["Launchpads"]
        self.rocketsLaunched = jsonDict["rocketsLaunched"]
    
    def buildRocket(self):
        self.rocketBuildQueue.put("rocket")
        self.money -= self.rocketCost
    
    async def handleVAB(self):
        try:
            while True:
                toBuild = await self.rocketBuildQueue.get()
                if toBuild == "rocket":
                    await asyncio.sleep(self.rocketBuildTime)
                    self.rocketLaunchQueue.put("rocket")
        except asyncio.CancelledError:
            # clean shutdown if cancelled
            return
    
    async def handleLaunchPad(self):
        try:
            while True:
                rocket = await self.rocketLaunchQueue.get()
                payload = await self.payloadQueue.get()
                if True:
                    await asyncio.sleep(5)
                    self.rocketsLaunched += 1
        except asyncio.CancelledError:
            # clean shutdown if cancelled
            return