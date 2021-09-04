import Connection



class Server:

    def __init__(self, eventPort: int, replyPort: int):
        self.eventConnection = Connection.EventSender(eventPort)
        self.requestConnection = Connection.RequestReceiver(replyPort)