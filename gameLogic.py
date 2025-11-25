import saves
import asyncio
from time import time
import asyncHandling

class World:
    def __init__(self, jsonDict):
        self.money = int(jsonDict["money"]) # casting value for myPy to accept typing
        # this can be used later if changes are needed to structure handling
        # self.infrastructure = dict([(body, [structure for structure in structures]) for body,structures in jsonDict["infrastructure"].items()])
        self.infrastructure = jsonDict["infrastructure"]

defaultSave = {
    "money":1_000_000,
    "infrastructure":{
        "earth":[
            {"type":"VAB", "level":1},
            {"type":"launchPad","level":1}
            ]
    }
}

class GameHandler:
    def __init__(self, saveFilename):
        self.world = World(saves.load(saveFilename, defaultSave))
        self.lastTick = time()
        self.asyncHandler = asyncHandling.handler(self.tick, self.handleInput)
        self.input = self.asyncHandler.inputQueue.put_nowait
        self.running = True
    
    def run(self):
        asyncio.run(self.main())

    def tick(self):
        startTime = time()
        deltaT=startTime-self.lastTick
        self.lastTick = startTime
    
    def launchRocket(self):
        pass # I have not thought this game through at all, and yet here I am: possibly closer that I have ever been to completion

    def handleInput(self, command):
        match command:
            case ["close"]:
                self.running = False
            case ["launch"]:
                self.launchRocket()
            case _:
                pass