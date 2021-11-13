from typing import Callable
import tkinter as tk

from .event import Event
from .eventQueue import EventQueue
from .eventLoop import EventLoop, ThreadedLoop, TkinterLoop



class EventNotFound(Exception):
    
    def __init__(self, eventType: Event, message: str) -> None:
        super().__init__(message)
        self.message = message
        self.eventType = eventType

class EventHandler:

    def __init__(self) -> None:
        self.queues: dict[str, EventQueue] = {} 

        self.loops: dict[str, EventLoop] = {}

    def handleEvent(self, eventType: Event, eventData) -> None:
        if not eventType.name in self.queues:
            raise EventNotFound(eventType, f"No listener defined for event {eventType.name}")

        queue = self.queues[eventType.name]
        if queue.full():
            return False, f"queue for event {eventType.name} is full"

        queue.put(eventData)
        return True, "OK"

    def addEvent(self, eventType: Event, maxQueueSize: int = 3) -> None:
        if eventType.name in self.queues:
            # TODO: raise error here
            return

        self.queues[eventType.name] = EventQueue(maxQueueSize)

    def addEventLoop(self, name: str, timeout: float = 1) -> None:
        if name in self.loops:
            # TODO: add error handling
            return

        loop = ThreadedLoop(timeout)
        self.loops[name] = loop

    def addTkinterEventLoop(self, name: str, app: tk.Tk, timeout: float = 1) -> None:
        if name in self.loops:
            # TODO: add error handling
            return

        loop = TkinterLoop(app, timeout)
        self.loops[name] = loop

    def setEventHandler(self, loopName: str, eventType: Event, handler: Callable) -> None:
        if not loopName in self.loops:
            print("no loop with name: ", loopName)
            return

        if not eventType.name in self.queues:
            raise EventNotFound(eventType, f"No listener defined for event {eventType.name}")

        queue = self.queues[eventType.name]

        self.loops[loopName].addEvent(queue, handler)

    def startLoop(self, loopName: str):
        if not loopName in self.loops:
            print("no loop with name: ", loopName)
            return
        
        self.loops[loopName].start()

        
    # def setEventHandler(self, eventType: Event, eventHandler: Callable, handle: Callable, *args) -> None:
    #     if not eventType.name in self.queues:
    #         raise EventNotFound(eventType, f"event {eventType.name} has not been added yet. Please use eventHandler.addEvent")

    #     self.handleEvent(self.queues[eventType.name], eventHandler, handle, *args)
        
    # def handleEvent(self, queue: EventQueue, eventHandler: Callable, handle: Callable, *args) -> None:
    #     if not queue.empty():
    #         eventHandler(queue.get())

    #     handle(*args, self.handleEvent, queue, eventHandler, handle, *args)