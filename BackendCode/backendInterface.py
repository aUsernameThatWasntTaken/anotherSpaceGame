# typing
from __future__ import annotations
from typing import Type, Protocol

#mine
from BackendCode.gameLogic import GameHandler
from BackendCode.errors import StopGame,SaveAndQuit
import BackendCode.saves as saves

# other
from time import time


# imports for frontend convenience
from BackendCode.errors import NotEnoughMoney
from BackendCode.saves import getTechTree

class GUIhandler(Protocol):
    def __init__(self, gameHandler: Backend): ...
    def update(self, gameHandler: Backend, deltaTime): ...

GUIClass = GUIhandler

class Backend:
    def __init__(self, saveFilename):
        self.lastTick = time()
        self.handler = GameHandler(saveFilename)
        self.payloadFuncs = self.handler.payloadFuncs

        world = self.handler.world
        self.getWorldStats = world.getStats
        self.getMoney = world.getMoney

    def run(self, GUIClass: Type[GUIhandler]):
        GUI = GUIClass(self)
        try:
            while True:
                startTime = time()
                self.handler.tick()

                deltaT=startTime-self.lastTick
                self.lastTick = startTime

                GUI.update(self, deltaT)
        except StopGame:
            pass
        except SaveAndQuit as e:
            saves.saveGame(self.handler.world, e.file)