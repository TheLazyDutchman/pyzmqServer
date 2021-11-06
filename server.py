from dataclasses import dataclass, field
from typing import Callable
from time import sleep

import threading

from .events.event import Event
from .events.eventHandler import EventHandler
from .events.eventLoop import EventLoop
from . import connection




class GroupNotFoundError(Exception):

    def __init__(self, groupName: str, message: str):
        self.groupName = groupName
        super().__init__(message)

class ClientNotFoundError(Exception):

    def __init__(self, groupName: str, clientName: str, message: str):
        self.groupName = groupName
        self.clientName = clientName
        super().__init__(message)

@dataclass
class ClientConnection:
    name: str
    connection: connection.RequestSender

@dataclass
class Group:
    name: str
    clients: dict[str, ClientConnection] = field(default_factory=dict)

class Server:

    def __init__(self, eventPort: int, replyPort: int, clientType: type[ClientConnection] = ClientConnection):
        self.eventConnection = connection.EventSender(eventPort)
        self.requestConnection = connection.RequestReceiver(replyPort, daemon = False)

        self.clientType = clientType

        self.eventLoops: dict[str, EventLoop] = {}

        self.groups: dict[str, Group] = {}
        self.groups["main"] = Group("main")

        self.requestHandler = EventHandler()

        self.requestConnection.SetCallback(self.requestHandler.handleEvent)

        self.requestHandler.addEventLoop("main", 1)

        joinGroupEvent = Event("join group")
        self.requestHandler.addEvent(joinGroupEvent)


        joinThread = threading.Thread(
            target = self.requestHandler.setEventHandler, 
            args = (
                joinGroupEvent,
                self.joinGroup,
                self.after,
                100
                ))
        joinThread.setDaemon(True)
        joinThread.start()

    def joinGroup(self, eventData):
        groupName, clientName, clientIp, clientRequestRecievePort = eventData
        group = self.getGroup(groupName)

        conn = connection.RequestSender(clientIp, clientRequestRecievePort)
        group.clients[clientName] = self.clientType(clientName, conn)

    def SendEvent(self, target: str, data):
        self.eventConnection.SendMessage(target, data)

    def SendRequest(self, groupName: str, clientName: str, requestType: str, data):
        client = self.getClient(groupName, clientName)

        event = Event(requestType)
        reply = client.connection.SendMessage(event, data)

        return reply

    def addRequestType(self, name: str):
        self.requestHandler.addEvent(Event(name))

    def setRequestHandler(self, requestType: str, requestHandler: Callable, handle: Callable, *args):
        self.requestHandler.setEventHandler(Event(requestType), requestHandler, handle, *args)

    def getGroup(self, groupName: str) -> Group:
        if not groupName in self.groups:
            raise GroupNotFoundError(groupName, f"Could not find group '{groupName}'")

        return self.groups[groupName]

    def getClient(self, groupName: str, clientName: str) -> ClientConnection:
        try:
            group = self.getGroup(groupName)

            if not clientName in group.clients:
                raise ClientNotFoundError(groupName, clientName, f"Could not find client '{clientName}' in group '{groupName}'")

            return group.clients[clientName]

        except GroupNotFoundError:
            raise ClientNotFoundError(groupName, clientName, f"could not find group '{groupName}' while searching for client {clientName}")
