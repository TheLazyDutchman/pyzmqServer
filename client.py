from typing import Callable

from . import Connection
from .events.event import Event
from .events.eventHandler import EventHandler
import socket



class Client:

    def __init__(self, serverIp: str, eventPort: int, requestSendPort: int, requestReceivePort: int):
        self.eventConnection = Connection.EventReceiver(serverIp, eventPort)
        self.requestSendConnection = Connection.RequestSender(serverIp, requestSendPort)
        self.requestReceiveConnection = Connection.RequestReceiver(requestReceivePort)

        hostName = socket.gethostname()
        clientIp = socket.gethostbyname(hostName)
        

        joinGroupEvent = Event("join group")

        groupName = "main"
        clientName = "client"

        self.eventHandler = EventHandler()

        self.requestReceiveConnection.SetCallback(self.eventHandler.handleEvent)


        eventData = groupName, clientName, clientIp, requestReceivePort
        self.requestSendConnection.SendMessage(joinGroupEvent, eventData)

    def SetEventCallback(self, eventCallback: Callable) -> None:
        self.eventConnection.SetCallback(eventCallback)

    def AddRequestListener(self, name: str, listener: Callable):
        self.eventHandler.addEventListener(Event(name), listener)

    def SendRequest(self, requestType: str, data):
        event = Event(requestType)
        reply = self.requestSendConnection.SendMessage(event, data)

        return reply

    def Subscribe(self, topic: str):
        self.eventConnection.Subscribe(topic)
