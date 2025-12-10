# typing
from __future__ import annotations
from typing import Type, Protocol

#mine
from BackendCode.gameLogic import GameHandler
import BackendCode.saves as saves

# other
from time import time


# imports for frontend convenience
from BackendCode.errors import NotEnoughMoney, StopGame, SaveAndQuit
from BackendCode.saves import getTechTree

class Backend:
    def __init__(self, saveFilename):
        self.lastTick = time()
        self.handler = GameHandler(saveFilename)
        self.payloadFuncs = self.handler.payloadFuncs
        self.tick = self.handler.tick

        world = self.handler.world
        self.getWorldStats = world.getStats
        self.getMoney = world.getMoney
        self.buildRocket = world.buildRocket

    def save(self, fileName):
        saves.saveGame(self.handler.world, fileName)