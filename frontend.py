from time import time

from BackendCode.backendInterface import Backend, StopGame, NotEnoughMoney, getTechTree

from FrontendCode.GUIhandlerClass import GUIhandler
from FrontendCode.pyGameWrapper import SCREEN_H, SCREEN_W

# note for future us: this was 849 lines at one point

TECH_TREE = getTechTree()

saveFile = "None"
backend = Backend(saveFile)
guihandler = GUIhandler(backend, TECH_TREE)
lastTick = time()
try:
    while True:
        currTime = time()
        dt = currTime-lastTick
        lastTick = currTime

        backend.tick()
        guihandler.update(backend, dt)
except StopGame:
    pass