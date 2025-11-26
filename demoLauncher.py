from gameLogic import GameHandler

while True:
    fileName = input("Save file name (do not include file extension): ")
    try:
        handler = GameHandler(fileName)
    except FileNotFoundError:
        print("File does not exist. For a new save, type \"None\"")
    else:
        break

isRunning = True

def updateGUI(gameHandler):
    pass

def getIsRunning():
    return isRunning

handler.run(updateGUI, getIsRunning)