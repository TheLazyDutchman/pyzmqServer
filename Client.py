from typing import Callable
import Connection



class Client:

    def __init__(self, serverIp: str, eventPort: int, requestSendPort: int, requestReceivePort: int):
        self.eventConnection = Connection.EventReceiver(serverIp, eventPort)
        self.requestSendConnection = Connection.RequestSender(serverIp, requestSendPort)
        self.requestReceiveConnection = Connection.RequestReceiver(requestReceivePort)

    def SetEventCallback(self, eventCallback: Callable) -> None:
        self.eventConnection.SetCallback(eventCallback)

    def SetRequestCallback(self, requestCallback: Callable) -> None:
        self.requestReceiveConnection.SetCallback(requestCallback)
