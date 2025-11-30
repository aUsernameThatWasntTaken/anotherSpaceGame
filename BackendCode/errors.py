class StopGame(Exception):
    def __init__(self):
        pass

class SaveAndQuit(Exception):
    def __init__(self, saveFileName: str):
        self.file = saveFileName

class NotEnoughMoney(Exception):
    def __init__(self, cost:int, difference: int):
        self.itemCost=cost
        self.itemCostDifference = difference