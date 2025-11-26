from enum import Enum
import saves
import asyncio
from time import time
import asyncHandling


class GameHandler:
    """Contains code to handle commands and to init the asyncHandler"""
    def __init__(self, saveFilename):
        self.world = saves.getWorld(saveFilename)
        self.lastTick = time()
        self.asyncHandler = asyncHandling.handler(self.tick, self.handleInput)
        self.input = self.asyncHandler.inputQueue.put_nowait
        self.isRunning = lambda: False
    
    def run(self, updateGUI, isRunning):
        self.updateGUI = updateGUI
        self.isRunning = isRunning
        asyncio.run(self.asyncHandler.main())

    def tick(self):
        #will handle things like passive income
        startTime = time()
        deltaT=startTime-self.lastTick
        self.lastTick = startTime
    
    def launchRocket(self):
        self.world.buildRocket()

    def handleInput(self, command):#to be deleted, I think.
        match command:
            case ["launch"]:
                self.launchRocket()
            case _:
                pass