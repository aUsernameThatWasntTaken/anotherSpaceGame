from BackendCode.events import handler as EventHandler
from BackendCode.events import Event, buildRocket, launchRocket
from BackendCode.techtree import Unlocks

class Queues:
    def __init__(self):
        self.build = []
        self.launch = []
        self.payload = []
    def getLengths(self):
        return {
            "build"  :len(self.build),
            "launch" :len(self.launch),
            "payload":len(self.payload)
        }

class World:
    def __init__(self, jsonDict):
        self.rocketBuildTime = 10 # seconds with a Lvl1 VAB
        self.rocketCost = 1000
        self.queues = Queues()
        self.readWorldData(jsonDict)
    
    def readWorldData(self, jsonDict):
        self.money = int(jsonDict["money"]) # casting value for myPy to accept typing
        self.vABlevel = int(jsonDict["infrastructure"]["VAB"])
        self.pads = int(jsonDict["infrastructure"]["Launchpads"])
        self.unlocks = Unlocks(jsonDict["unlocks"])
        self.eventHandler = EventHandler(jsonDict["events"])
        self.VABinUse = buildRocket in [event.name for event in self.eventHandler.events] #if any event is called BuildRocket
        self.padsInUse = len([event for event in self.eventHandler.events if event.name == launchRocket])
    
    def tick(self):
        self.VABtick()
        self.updatePads()
    def getStats(self):
        return {"money":self.money,
                "padsinUse":self.padsInUse,
                "queues":self.queues.getLengths()}
    
    def buildRocket(self):
        self.queues.build.append("rocket")
        self.money -= self.rocketCost

    def updatePads(self):
        for i in range(self.pads - self.padsInUse): #for each pad not in use
            self.padTick()

    def padTick(self):
        if len(self.queues.launch) == 0 and len(self.queues.payload) == 0:
            return # no rocket or no payload available
        rocket = self.queues.launch.pop(0)
        payload = self.queues.payload.pop(0)
        def endLaunch():
            self.padsInUse -=1
            payload() # calls payload reward

        self.padsInUse +=1
        self.eventHandler.add(Event(launchRocket, endLaunch, 5))
    
    def VABtick(self):
        if self.VABinUse:
            return
        try:
            toBuild = self.queues.build.pop(0)
        except IndexError:
            return
        def rollOutRocket():
            self.queues.launch.put_nowait(toBuild)
            self.VABinUse = False
        self.eventHandler.add(Event(buildRocket,rollOutRocket,self.rocketBuildTime))