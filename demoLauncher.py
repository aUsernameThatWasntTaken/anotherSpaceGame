from gameLogic import GameHandler

fileName = input("Save file name (do not include file extension): ")
with GameHandler(fileName) as gh:
    pass