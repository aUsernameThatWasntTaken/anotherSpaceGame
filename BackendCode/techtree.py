from typing import Callable

otherTechs: list[str] = []

class Technology:
    def __init__(self, req: list[str], repeatable: bool, cost = 0, costFunc: Callable[[int], int]|None = None):
        """Takes costFunc(x), where x is the level to upgrade to"""
        if costFunc is None:
            self.getCost: Callable[[int], int] = lambda _: cost
        else:
            self.getCost = costFunc
        self.req = req
        self.repeatable = repeatable
            

technologies = {
    "rocketSize":Technology([],True,costFunc=(lambda x: 100*(2**x)))
}

class Unlocks:
    def __init__(self, unlockDict: dict[str,int]):
        self.rocketSize = int(unlockDict["rocketSize"])
        self.all = {tech:unlockDict[tech] for tech in technologies.keys()}

    def cost(self, tech: str):
        """returns the tech cost of the next level of the unlock"""
        return technologies[tech].getCost(self.all[tech])