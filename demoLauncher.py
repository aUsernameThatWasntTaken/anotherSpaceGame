from gameLogic import GameHandler
import tkinter

root = tkinter.Tk()
root.title("Rocket Clicker (to be renamed) Demo")

while True:
    fileName = input("Save file name (do not include file extension): ")
    try:
        handler = GameHandler(fileName)
    except FileNotFoundError:
        print("File does not exist. For a new save, type \"None\"")
    else:
        break

isRunning = True
class GUI:
    def __init__(self, gameHandler: GameHandler):
        tkinter.Label(root, text="Welcome to rocket Clicker (to be renamed)").grid(row=0,column=0)
        tkinter.Button(root, text="build and launch rocket", command=lambda: gameHandler.launchRocket).grid(row=1,column=0)
        self.moneyStringVar = tkinter.StringVar(root, "Money:")
        tkinter.Label(root, textvariable=self.moneyStringVar).grid(row=2,column=0)
        self.launchComplexStatsVar = tkinter.StringVar(root, "Launch complex stats:")
        tkinter.Label(root, textvariable=self.launchComplexStatsVar).grid(row=3,column=0)
        #TODO: continue:

    def updateGUI(self, gameHandler: GameHandler):
        pass

handler.run(GUI)