from dataclasses import dataclass
from threading import Thread
from time import sleep
from typing import Callable

from .eventQueue import EventQueue



@dataclass
class queueHandler:
    queue: EventQueue
    function: Callable

class EventLoop:

    def __init__(self, timeout: float) -> None:
        self.timeout = timeout

        self.handlers: list[queueHandler] = []

    def addEvent(self, queue: EventQueue, function: Callable) -> None:
        self.handlers.append(queueHandler(queue, function))

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