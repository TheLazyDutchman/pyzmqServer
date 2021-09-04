import Connection



class Client:

    def __init__(self, serverIp: str, eventPort: int, requestSendPort: int, requestReceivePort):
        self.eventConnection = Connection.EventReceiver(serverIp, eventPort)
        self.requestSendConnection = Connection.RequestSender(serverIp, requestSendPort)
        self.requestReceiveConnection = Connection.RequestReceiver(requestReceivePort)
