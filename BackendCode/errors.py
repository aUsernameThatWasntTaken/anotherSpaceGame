class StopGame(Exception):
    def __init__(self):
        pass

class SaveAndQuit(Exception):
    def __init__(self, saveFileName: str):
        self.file = saveFileName