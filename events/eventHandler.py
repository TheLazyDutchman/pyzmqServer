from typing import Callable

from .event import Event



class EventNotFound(Exception):
    
    def __init__(self, eventType: Event, message: str) -> None:
        super().__init__(message)
        self.message = message
        self.eventType = eventType

class EventHandler:

    def __init__(self) -> None:
        self.listeners: dict[Event, list[Callable]] = {} 

    def handleEvent(self, eventType: Event, eventData) -> None:
        if not eventType.name in self.listeners:
            raise EventNotFound(eventType, f"No listeners defined for event {eventType.name}")

        answer = None
        for listener in self.listeners[eventType.name]:
            currentAnswer = listener(eventData)
            if not currentAnswer == None:
                answer = currentAnswer

        return answer
        
    def addEventListener(self, eventType: Event, listener: Callable) -> None:
        if not eventType.name in self.listeners:
            self.listeners[eventType.name] = []

        self.listeners[eventType.name].append(listener)