from abc import ABC, abstractmethod
from dataclasses import dataclass
from threading import Thread
from time import sleep
from typing import Callable
import tkinter as tk

from .eventQueue import EventQueue



@dataclass
class queueHandler:
    queue: EventQueue
    function: Callable

class EventLoop(ABC):

    def __init__(self, timeout: float) -> None:
        self.timeout = timeout

        self.handlers: list[queueHandler] = []

    def addEvent(self, queue: EventQueue, function: Callable) -> None:
        self.handlers.append(queueHandler(queue, function))

    @abstractmethod
    def start(self) -> None:
        pass

class ThreadedLoop(EventLoop):

    def loop(self) -> None:
        while True:

            for handler in self.handlers:
                if handler.queue.empty():
                    continue
                
                event = handler.queue.get(block=False)

                handler.function(event)

            sleep(self.timeout)

    def start(self) -> None:
        loopThread = Thread(target=self.loop, daemon=True)

        loopThread.start()

class TkinterLoop(EventLoop):

    def __init__(self, app: tk.Tk, timeout: float) -> None:
        super().__init__(timeout)
        self.app = app

    def loop(self) -> None:
        for handler in self.handlers:
            if handler.queue.empty():
                continue
            
            event = handler.queue.get(block=False)

            handler.function(event)

        self.app.after(self.timeout * 1000, self.loop)

    def start(self) -> None:
        self.app.after(self.timeout * 1000, self.loop)