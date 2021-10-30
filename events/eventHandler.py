from typing import Callable

from .event import Event
from .eventQueue import EventQueue, QueueFull



class EventNotFound(Exception):
    
    def __init__(self, eventType: Event, message: str) -> None:
        super().__init__(message)
        self.message = message
        self.eventType = eventType

class EventHandler:

    def __init__(self) -> None:
        self.queues: dict[Event, EventQueue] = {} 

    def handleEvent(self, eventType: Event, eventData) -> None:
        if not eventType.name in self.queues:
            raise EventNotFound(eventType, f"No listener defined for event {eventType.name}")

        queue = self.queues[eventType.name]
        if queue.full():
            return False, f"queue for event {eventType.name} is full"

        queue.put(eventData)
        return True, "OK"

    def addEvent(self, eventType: Event, maxQueueSize: int = 3):
        if eventType.name in self.queues:
            # TODO: raise error here
            return

        self.queues[eventType.name] = EventQueue(maxQueueSize)
        
    # def setEventListener(self, eventType: Event, listener: Callable) -> None:
    #     # if not eventType.name in self.listeners:
    #     #     # TODO: raise error here
    #     #     return

    #     # self.queues[eventType.name].append(listener)
    #     pass