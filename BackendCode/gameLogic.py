#Typing:
from __future__ import annotations
from typing import Protocol, Type

#other
import asyncio
from time import time

#other code files:
import BackendCode.asyncHandling as asyncHandling
import BackendCode.saves as saves


class StopGame(RuntimeError):
    def __init__(self):
        pass

class GameHandler:
    """Contains code to handle commands and to init the asyncHandler"""
    def __init__(self, saveFilename):
        self.world = saves.getWorld(saveFilename)
        self.lastTick = time()
        self.asyncHandler = asyncHandling.handler(self.tick, self.handleInput)
        self.input = self.asyncHandler.inputQueue.put_nowait
        self.isRunning = lambda: False
    
    def run(self, GUIobject):
        self.updateGUI = GUIobject.update()
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