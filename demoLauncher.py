from gameLogic import GameHandler

while True:
    fileName = input("Save file name (do not include file extension): ")
    try:
        handler = GameHandler(fileName)
    except FileNotFoundError:
        print("File does not exist. For a new save, type \"None\"")
    else:
        break

with handler as gh:
    pass