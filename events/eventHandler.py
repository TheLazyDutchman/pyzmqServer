from typing import Callable

from .event import Event



class EventNotFound(Exception):
    
    def __init__(self, eventType: Event, message: str) -> None:
        super().__init__(message)
        self.eventType = eventType

class EventHandler:

    def __init__(self) -> None:
        self.listeners: dict[Event, list[Callable]] = {} 

    def handleEvent(self, eventType: Event, eventData) -> None:
        if not eventType in self.listeners:
            raise EventNotFound(eventType, f"No listeners defined for event {eventType}")

        for listener in self.listeners[eventType]:
            listener(eventData)

    def addEventListener(self, eventType: Event, listener: Callable) -> None:
        if not eventType in self.listeners:
            self.listeners[eventType] = []

        self.listeners[eventType].append(listener)