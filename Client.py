import Connection



class Client:

    def __init__(self, serverIp: str, eventPort: int, serverRequestPort: int):
        self.eventConnection = Connection.EventReceiver(serverIp, eventPort)
        self.requestConnection = Connection.RequestSender(serverIp, serverRequestPort)