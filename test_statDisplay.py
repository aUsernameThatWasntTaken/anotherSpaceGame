from BackendCode.gameLogic import GameHandler
from BackendCode.errors import StopGame

result = {}

class GUIhandler:
    def __init__(self, _: GameHandler): 
        self.i = 0

    def update(self, gameHandler: GameHandler, _):
        self.i +=1
        gameHandler.world.buildRocket()
        if self.i == 10:#wait until tenth frame
            global result
            result = gameHandler.world.getStats()
            raise StopGame()

GameHandler("None").run(GUIhandler)

def test_pads():
    assert result["pads"] == {"awaitingRocket":1,"awaitingPayload":0,"launching":0}

def test_queues():
    assert result["queues"] == {"build":9,"launch":0,"payload":0}