import asyncio

from BackendCode.events import handler as EventHandler
from BackendCode.events import Event
from BackendCode.techtree import Unlocks

class PadStats:
    def __init__(self):
        self.launching = 0
        self.awaitingRocket = 0
        self.awaitingPayload = 0
    def getDict(self):
        return {
            "awaitingRocket":self.awaitingRocket,
            "awaitingPayload":self.awaitingPayload,
            "launching":self.launching
        }

class Queues:
    def __init__(self):
        self.build = []
        self.launch = asyncio.Queue()
        self.payload = asyncio.Queue()
    def getLengths(self):
        return {
            "build"  :self.build  .qsize(),
            "launch" :self.launch .qsize(),
            "payload":self.payload.qsize()
        }

class World:
    def __init__(self, jsonDict):
        self.rocketBuildTime = 10 # seconds with a Lvl1 VAB
        self.rocketCost = 1000
        self.queues = Queues()
        self.readWorldData(jsonDict)
        self.padStats = PadStats()
    
    def getStats(self):
        return {"money":self.money,
                "pads":self.padStats.getDict(),
                "queues":self.queues.getLengths()}
    
    def readWorldData(self, jsonDict):
        self.money = int(jsonDict["money"]) # casting value for myPy to accept typing
        self.vABlevel = jsonDict["infrastructure"]["VAB"]
        self.pads = jsonDict["infrastructure"]["Launchpads"]
        self.unlocks = Unlocks(jsonDict["unlocks"])
        self.eventHandler = EventHandler(jsonDict["events"])
    
    def buildRocket(self):
        self.queues.build.append("rocket")
        self.money -= self.rocketCost
    
    async def handleVAB(self):
        raise DeprecationWarning("Just call handleOneBuild every frame instead")
    
    async def handleLaunchPad(self):
        try:
            while True:
                await self.handleOneLaunch()
        except asyncio.CancelledError:
            # clean shutdown if cancelled
            return

    async def handleOneLaunch(self):
        self.padStats.awaitingRocket +=1
        rocket = await self.queues.launch.get()
        self.padStats.awaitingRocket -=1

        self.padStats.awaitingPayload +=1
        payload = await self.queues.payload.get()
        self.padStats.awaitingPayload -=1

        if True: # wait, what?
            self.padStats.launching +=1
            await asyncio.sleep(5)
            self.padStats.launching -=1
            self.rocketsLaunched += 1
    
    def handleOneBuild(self):
        try:
            toBuild = self.queues.build.pop(0)
        except IndexError:
            return
        def rollOutRocket():
            self.queues.launch.put_nowait(toBuild)
        self.eventHandler.events.append(Event("BuildRocket",rollOutRocket,self.rocketBuildTime))