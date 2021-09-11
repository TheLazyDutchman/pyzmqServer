from typing import Callable
import Connection




class GroupNotFoundError(Exception):

    def __init__(self, groupName: str, message: str):
        self.groupName = groupName
        super().__init__(message)

class ClientNotFoundError(Exception):

    def __init__(self, groupName: str, clientName: str, message: str):
        self.groupName = groupName
        self.clientName = clientName
        super().__init__(message)

class ClientConnection:
    name: str
    connection: Connection.RequestSender

class Group:
    name: str
    clients: dict[str, ClientConnection]

class Server:

    def __init__(self, eventPort: int, replyPort: int):
        self.eventConnection = Connection.EventSender(eventPort)
        self.requestConnection = Connection.RequestReceiver(replyPort)

        self.groups: dict[str, Group] = []

    def SendRequest(self, groupName: str, clientName: str, requestType: str, data):
        client = self.getClient(groupName, clientName)

        reply = client.connection.SendMessage(requestType, data)

        return reply

    def SetRequestCallback(self, requestCallback: Callable):
        self.requestConnection.SetCallback(requestCallback)

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
