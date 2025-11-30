#Typing:
from __future__ import annotations
from typing import Protocol, Type

#other
from time import time

#my modules:
import BackendCode.saves as saves
from BackendCode.errors import StopGame, SaveAndQuit


class GUIhandler(Protocol):
    def __init__(self, gameHandler: GameHandler): ...
    def update(self, gameHandler: GameHandler, deltaTime): ...

class GameHandler:
    """Contains code to handle commands and to init the asyncHandler"""
    def __init__(self, saveFilename):
        self.world = saves.getWorld(saveFilename)
        self.lastTick = time()
        self.payloadFuncs = {
            "com":self.queueComPayload,
            "sci":self.queueSciPayload
        }
    
    def run(self, GUIClass: Type[GUIhandler]):
        self.GUI = GUIClass(self)
        try:
            while True:
                self.tick()
        except StopGame:
            pass
        except SaveAndQuit as e:
            saves.saveGame(self.world, e.file)

    def tick(self):
        #will handle things like passive income and GUI
        startTime = time()
        deltaT=startTime-self.lastTick
        self.lastTick = startTime
        self.GUI.update(self, deltaT)
        if self.world.money<0:
            raise RuntimeError("Money went negative after your last action. Please contact developer.")
    
    def buyLaunchPad(self):
        self.world.spend(1000)
        self.world.pads+=1
    
    def upgradeVAB(self):
        self.world.spend(10000)
        self.world.vABlevel+=1

    def launchRocket(self): # legacy name stays for now
        self.world.buildRocket()
    
    def queueComPayload(self):
        self.world.queues.payload.append("commercial")
    
    def queueSciPayload(self):
        self.world.spend(100)
        self.world.queues.payload.append("scientific")