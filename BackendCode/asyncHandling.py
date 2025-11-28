import asyncio

class handler:
    """Handles the input Queue and tick loop to allow input while the game runs."""
    def __init__(self, tickFunc, handleInput):
        self.tick = tickFunc
        self.handleInput = handleInput
        self.inputQueue = asyncio.Queue()

    async def main(self): # try blocks by chatgpt
        """starts gameloop and handles input"""
        tickTask = asyncio.create_task(self._tick_loop(1.0))
        try:
            while True:
                #handle input
                command = await self.inputQueue.get()
                self.handleInput(command)
        finally:#execute no matter what to allow cleanup
            tickTask.cancel()
            try:
                await tickTask
            except asyncio.CancelledError:
                pass

    async def _tick_loop(self, interval: float): #also chatGPT
        """Background game tick loop running while waiting for input."""
        try:
            while True:
                self.tick()
                await asyncio.sleep(interval)
        except asyncio.CancelledError:
            # clean shutdown if cancelled
            return