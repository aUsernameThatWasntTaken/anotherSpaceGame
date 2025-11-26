from enum import Enum
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
        self.vABSpeed = sum([item["level"] for item in self.infrastructure["earth"] if item["type"]=="VAB"])

defaultSave = {
    "money":1_000_000,
    "infrastructure":{
        "earth":[
            {"type":"VAB", "level":1},
            {"type":"launchPad","level":1}
            ]
    }
}

class Rockets(Enum):
    suborbital = 0 

# in seconds with one Lvl1 VAB:
rocketBuildTime = {Rockets.suborbital:10}

class GameHandler:
    """Contains code to handle commands and to init the asyncHandler"""
    def __init__(self, saveFilename):
        self.selectedRocket = Rockets.suborbital
        self.world = World(saves.load(saveFilename, defaultSave))
        self.lastTick = time()
        self.asyncHandler = asyncHandling.handler(self.tick, self.handleInput)
        self.input = self.asyncHandler.inputQueue.put_nowait
        self.running = True
    
    def __enter__(self):
        self.mainTask = asyncio.create_task(self.asyncHandler.main())
    
    def __exit__(self, exc_type, exc_value, exc_trace):
        asyncio.run(self.asyncExit())
    
    async def asyncExit(self):
        self.mainTask.cancel()
        try:
            await self.mainTask
        except asyncio.CancelledError:
            pass

    def tick(self):
        startTime = time()
        deltaT=startTime-self.lastTick
        self.lastTick = startTime
    
    async def launchRocket(self):
        await asyncio.sleep(rocketBuildTime[self.selectedRocket]/self.world.vABSpeed)
        await asyncio.sleep(10)
        print("rocket launched")

    def handleInput(self, command):
        match command:
            case ["launch"]:
                self.launchRocket()
            case _:
                pass