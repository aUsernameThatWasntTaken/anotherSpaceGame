import asyncio

class PadStats:
    def __init__(self):
        self.empty = 0
        self.awaitingRocket = 0
        self.awaitingPayload = 0
    def __dict__(self):
        return {
            "empty":self.empty,
            "awaitingRocket":self.awaitingRocket,
            "awaitingPayload":self.awaitingPayload
        }

class Queues:
    def __init__(self):
        self.build = asyncio.Queue()
        self.launch = asyncio.Queue()
        self.payload = asyncio.Queue()

class World:
    def __init__(self, jsonDict):
        self.rocketBuildTime = 10 # seconds with a Lvl1 VAB
        self.rocketCost = 1000
        self.queues = Queues()
        self.readWorldData(jsonDict)
        self.padStats = PadStats()
    
    def getStats(self):
        return {"pads":dict(self.padStats),
                "queues":{}}
    
    def readWorldData(self, jsonDict):
        self.money = int(jsonDict["money"]) # casting value for myPy to accept typing
        self.vABlevel = jsonDict["infrastructure"]["VAB"]
        self.pads = jsonDict["infrastructure"]["Launchpads"]
    
    def buildRocket(self):
        self.queues.build.put_nowait("rocket")
        self.money -= self.rocketCost
    
    async def handleVAB(self):
        try:
            while True:
                toBuild = await self.queues.build.get()
                if toBuild == "rocket":
                    await asyncio.sleep(self.rocketBuildTime)
                    self.queues.launch.put_nowait("rocket")
        except asyncio.CancelledError:
            # clean shutdown if cancelled
            return
    
    async def handleLaunchPad(self):
        try:
            while True:
                rocket = await self.queues.launch.get()
                payload = await self.queues.payload.get()
                if True:
                    await asyncio.sleep(5)
                    self.rocketsLaunched += 1
        except asyncio.CancelledError:
            # clean shutdown if cancelled
            return