from typing import Callable
import tkinter as tk

from . import connection
from .events.event import Event
from .events.eventHandler import EventHandler
import socket



class Client:

    def __init__(self, serverIp: str, eventPort: int, requestSendPort: int, requestReceivePort: int):
        self.eventConnection = connection.EventReceiver(serverIp, eventPort)
        self.requestSendConnection = connection.RequestSender(serverIp, requestSendPort)
        self.requestReceiveConnection = connection.RequestReceiver(requestReceivePort)

        hostName = socket.gethostname()
        clientIp = socket.gethostbyname(hostName)
        

        joinGroupEvent = Event("join group")

        self.groupName = "main"
        self.clientName = "client"

        self.eventHandler = EventHandler()
        self.eventConnection.SetCallback(lambda _, data: self.eventHandler.handleEvent(data[0], data[1]))
        self.eventHandler.addEventLoop("main")
        self.eventHandler.startLoop("main")

        self.requestHandler = EventHandler()
        self.requestReceiveConnection.SetCallback(self.requestHandler.handleEvent)
        self.requestHandler.addEventLoop("main")
        self.requestHandler.startLoop("main")


        eventData = self.groupName, self.clientName, clientIp, requestReceivePort
        self.requestSendConnection.SendMessage(joinGroupEvent, eventData)



    def addRequestType(self, requestType: str):
        self.requestHandler.addEvent(Event(requestType))

    def setRequestHandler(self, eventType: str, requestHandler: Callable, loopName: str = "main"):
        self.requestHandler.setEventHandler(loopName, Event(eventType), requestHandler)

    def createRequestLoop(self, name: str, timeout: float = 1) -> None:
        self.requestHandler.addEventLoop(name, timeout)

    def createTkinterRequestLoop(self, name: str, app: tk.Tk, timeout: float = 1) -> None:
        self.requestHandler.addTkinterEventLoop(name, app, timeout)
        self.requestHandler.startLoop(name)


    def addEventType(self, eventType: str):
        self.eventHandler.addEvent(Event(eventType))

    def setEventHandler(self, eventType: str, eventHandler: Callable, loopName: str = "main"):
        self.eventHandler.setEventHandler(loopName, Event(eventType), eventHandler)

    def createEventLoop(self, name: str, timeout: float = 1) -> None:
        self.eventHandler.addEventLoop(name, timeout)



    def SendRequest(self, requestType: str, data):
        event = Event(requestType)
        reply = self.requestSendConnection.SendMessage(event, data)

        return reply

    def Subscribe(self, topic: str):
        self.eventConnection.Subscribe(topic)
