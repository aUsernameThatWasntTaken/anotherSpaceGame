from time import time

from BackendCode.backendInterface import StopGame, getTechTree, Backend

from FrontendCode.GUIhandlerClass import GUIhandler
import FrontendCode.helpers as helpers

# note for future us: this was 849 lines at one point, now mostly split between techTree.py, GUIhandlerClass.py and techTree.json
# I can not comprehend how Saahil wrapped his head around that. -Max

# Doesn't crash, but on my laptop it raises LOADS of UserWarnings and shows nothing (possibly offscreen), probably due to some resolution limitations. Please fix if possible

TECH_TREE = getTechTree()

saveFile = "None"
backend = Backend(saveFile) # AT NO POINT CAN THIS BE SET TO ANY OTHER VARIABLE, ONLY ITS METHODS. IT MUST BE PASSED AS AN ARGUMENT
# this is because python doesn't have pointers as far as I know, and doing the above would copy it, which we do not want.

guihandler = GUIhandler(backend, TECH_TREE)
lastTick = time()
try:
    while True: # Here, have the loop back, it's much better in your hands.
        currTime = time()
        dt = currTime-lastTick
        lastTick = currTime

        backend.tick()
        guihandler.update(backend, dt)
except StopGame:
    pass