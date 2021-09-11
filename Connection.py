from typing import Callable
import zmq
import pickle
import threading
from abc import ABC, abstractmethod

context = zmq.Context()


class Connection:
    socket: zmq.Socket




class EventSender(Connection):
    
    def __init__(self, port: int) -> None:
        self.socket = context.socket(zmq.PUB)
        self.socket.bind(f"tcp://*:{port}")

    def SendMessage(self, topic: str, data):
        data = pickle.dumps(data)

        self.socket.send_multipart((topic, data))

class RequestSender(Connection):
    
    def __init__(self, serverIp: str, port: int) -> None:
        self.socket = context.socket(zmq.REQ)
        self.socket.connect(f"tcp://{serverIp}:{port}")

    def SendMessage(self, requestType: str, data):
        data = pickle.dumps(data)

        reply = self.socket.send_multipart((requestType, data))

        return reply



class Reciever(ABC):

    callback: Callable = print

    def SetCallback(self, callback: Callable) -> None:
        self.callback = callback

    def start(self):
        loopThread = threading.Thread(target = self.startLoop)
        loopThread.daemon = True
        loopThread.start()

    @abstractmethod
    def startLoop(self):
        pass

class EventReceiver(Connection, Reciever):
    
    def __init__(self, serverIp: str, port: int) -> None:
        self.socket = context.socket(zmq.SUB)
        self.socket.connect(f"tcp://{serverIp}:{port}")

        self.start()

    def Subscribe(self, topic: str):
        self.socket.subscribe(topic)

    def startLoop(self):
        while True:

            topic, data = self.socket.recv_multipart()

            self.callback(topic, data)

class RequestReceiver(Connection, Reciever):
    
    def __init__(self, port: int) -> None:
        self.socket = context.socket(zmq.REP)
        self.socket.bind(f"tcp://*:{port}")

        self.start()

    def startLoop(self):
        while True:

            requestType, data = self.socket.recv_multipart()

            answer = self.callback(requestType, data)
            answer = pickle.dumps(answer)

            self.socket.send(answer)

