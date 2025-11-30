
"""
Adds events to replace async sleep, allowing you to put them in a save file.\n
\n
Example Usage:\n
await asyncio.sleep(self.rocketBuildTime)\n
rollOutRocket()\n
To this:\n
eventHandler.events.append(Event("BuildRocket",rollOutRocket,self.rocketBuildTime))
"""
from time import time
from typing import Callable, Any

#standardised Event Names:
buildRocket = "buildRocket"

class Event:
    """Works as is, but better to inherit and modify"""
    def __init__(self, name: str, func: Callable[[],Any], timeUntil: float):
        self.name = name
        self.func = func
        self.time = time()+timeUntil
    def getDict(event, stopTime):
        return {"name":event.name, "timeUntil":event.time-stopTime} 

def eventType(name, func: Callable[[],Any], timeUntil):
    def newEvent():
        return Event(name, func, timeUntil)
    return newEvent

type EventType = Callable[[],Event]
#for loading events at launch (a rather bad way to do this, as the functions are generalised, so info is lost, but alas)
defaultEventTypes: dict[str,EventType] = {}

class handler:
    def __init__(self, eventDicts) -> None:
        # for each eventDict, gets the eventType assigned to the name and makes an instance of it
        self.events = [defaultEventTypes[eventDict["name"]]() for eventDict in eventDicts] 

    def add(self, event):
        self.events.append(event)

    def update(self, currentTime) ->None:
        newEventsList: list[Event] = []
        for event in self.events:
            if event.time<currentTime:
                event.func()
            else:
                newEventsList.append(event)
        self.events = newEventsList
    
    def getDict(self, stopTime):
        return [event.getDict(stopTime) for event in self.events]