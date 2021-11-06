from typing import Callable

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

        groupName = "main"
        clientName = "client"

        self.eventHandler = EventHandler()
        self.eventConnection.SetCallback(self.eventHandler.handleEvent)
        self.eventHandler.addEventLoop("main")

        self.requestHandler = EventHandler()
        self.requestReceiveConnection.SetCallback(self.requestHandler.handleEvent)
        self.requestHandler.addEventLoop("main")


        eventData = groupName, clientName, clientIp, requestReceivePort
        self.requestSendConnection.SendMessage(joinGroupEvent, eventData)



    def addRequestType(self, requestType: str):
        self.requestHandler.addEvent(Event(requestType))

    def setRequestHandler(self, eventType: str, requestHandler: Callable, loopName: str = "main"):
        self.requestHandler.setEventHandler(loopName, Event(eventType), requestHandler)

    def createRequestLoop(self, name: str, timeout: float = 1) -> None:
        self.requestHandler.addEventLoop(name, timeout)


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
