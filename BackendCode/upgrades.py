from typing import Callable

otherUpgrades: list[str] = []

class Upgrade:
    def __init__(self, costFunc: Callable[[int], int]):
        """Takes costFunc(x), where x is the level to upgrade to"""
        self.getCost = costFunc
            

upgrades = {
    "rocketSize":Upgrade(lambda x: 100*(2**x))
}

class Unlocks:
    def __init__(self, unlockDict: dict[str,int]):
        self.rocketSize = int(unlockDict["rocketSize"])
        self.all = {tech:unlockDict[tech] for tech in upgrades.keys()}

    def cost(self, tech: str):
        """returns the tech cost of the next level of the unlock"""
        return upgrades[tech].getCost(self.all[tech])