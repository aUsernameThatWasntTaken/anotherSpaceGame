from time import time

from BackendCode.backendInterface import StopGame, getTechTree, Backend
from BackendCode.logging import log_warnings

from FrontendCode.GUIhandlerClass import GUIhandler

# Doesn't crash, but on my laptop it raises LOADS of UserWarnings and shows nothing (possibly offscreen)
# This is probably due to some resolution limitations. Please fix if possible
@log_warnings("log.txt")
def main():
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

main()