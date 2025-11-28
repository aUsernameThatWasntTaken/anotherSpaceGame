#Typing:
from __future__ import annotations
from typing import Protocol, Type

#other
import asyncio
from time import time

#other code files:
import BackendCode.asyncHandling as asyncHandling
import BackendCode.saves as saves


class GUIhandler(Protocol):
    def __init__(self, gameHandler: GameHandler): ...
    def update(self, gameHandler: GameHandler, deltaTime): ...

class GameHandler:
    """Contains code to handle commands and to init the asyncHandler"""
    def __init__(self, saveFilename):
        self.world = saves.getWorld(saveFilename)
        self.lastTick = time()
        self.asyncHandler = asyncHandling.handler(self.tick, self.handleInput)
        self.input = self.asyncHandler.inputQueue.put_nowait
        self.isRunning = lambda: False
        self.payloadFuncs = {
            "com":self.queueComPayload,
            "sci":self.queueSciPayload
        }
    
    def run(self, GUIClass: Type[GUIhandler]):
        self.GUI = GUIClass(self)
        asyncio.run(self.asyncHandler.main())

    def tick(self):
        #will handle things like passive income and GUI
        startTime = time()
        deltaT=startTime-self.lastTick
        self.lastTick = startTime
        self.GUI.update(self, deltaT)
    
    def launchRocket(self):
        self.world.buildRocket()
    
    def queueComPayload(self):
        self.world.payloadQueue.put("commercial")
    
    def queueSciPayload(self):
        self.world.money -= 100
        self.world.payloadQueue.put("scientific")