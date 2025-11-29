import asyncio
from BackendCode.WorldClass import World

class handler:
    """Handles the input Queue and tick loop to allow input while the game runs."""
    def __init__(self, tickFunc, handleInput, world: World):
        self.tick = tickFunc
        self.handleInput = handleInput
        self.inputQueue: asyncio.Queue = asyncio.Queue()
        routines = [world.handleVAB]+[world.handleLaunchPad for _ in range(world.pads)]
        self.tasks: list[asyncio.Task] = [asyncio.create_task(routine()) for routine in routines] #maybe try asyncio taskgroups

    async def main(self): # try blocks by chatgpt
        """starts gameloop and handles input"""
        try:
            while True:
                self.tick()
                await asyncio.sleep(1/60)

        finally:#execute no matter what to allow cleanup
            for task in self.tasks:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass