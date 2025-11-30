raise DeprecationWarning("Please do not")

import asyncio
from BackendCode.WorldClass import World
from BackendCode.errors import StopGame

class handler:
    """Handles the input Queue and tick loop to allow input while the game runs."""
    def __init__(self, tickFunc, world: World):
        self.tick = tickFunc
        self.routines = [world.handleLaunchPad for _ in range(world.pads)]

    async def main(self): # try blocks by chatgpt
        """starts gameloop and handles input"""
        tasks = [asyncio.create_task(routine()) for routine in self.routines] #maybe try asyncio taskgroups
        try:
            while True:
                self.tick()
                await asyncio.sleep(1/60)
        except StopGame:
            pass
        finally: #execute no matter what to allow cleanup
            for task in tasks:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass