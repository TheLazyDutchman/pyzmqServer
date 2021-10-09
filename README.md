# pyzmqServer
this is a python client-server connection library built on [pyzmq]("https://github.com/zeromq/pyzmq" "The python zmq library").
## Usage

[Server Usage](#Server-side "Goto Server side")

[Client Usage](#Client-side "Goto Client side")
### Server side
to use the server, you have to import the 'Server' class from 'pyzmqServer.server'.

#### Initialization

creating a server has three arguments.
* eventPort - the port where the clients can listen for server events.
* replyPort - the port where the server listens for requests from clients and .replys to them.
* clientType - the type the server uses to store a client.
    - default - 'pyzmqServer.server.ClientConnection'.
``` python
from pyzmqServer.server import Server

eventSendPort = 5555
requestRecvReplyPort = 5556

server = Server(eventSendPort, requestRecvReplyPort)
```
#### Events
the server has a built-in event listener for requests that are sent by the client.

 arguments:
 * name - the name of the event type to listen for.
 * listener - a callback to call when the event is received.
 ```python
server.AddRequestListener("MyEvent", myEvent.handle)
 ```
### Client side
to use the client, you need to import the 'Client' class from 'pyzmqServer.client'.
#### Initialization
creating a client has five arguments:
* serverIp - the IP address of the server as a string.
* eventPort - the port on the server where the client listens for server events.
* requestSendPort - the port on the server listens to which the client can send a request.
* requestReceivePort - the port where the client listens for requests send from the server.
``` python
from pyzmqServer.client import Client

serverIp = "127.0.0.1" # normally this would of course not be localhost but an actual server
eventRecvPort = 5555
requestSendPort = 5556
requestRecvReplyPort = 5557

client = Client(serverIp, eventRecvPort, requestSendPort, requestRecvReplyPort)
```

#### Events
the client has a built-in event listener for requests that are sent by the server.
 - [x] event handler for server requests.
 - [ ] event handler for server events.

 arguments:
 * name - the name of the event type to listen for.
 * listener - a callback to call when the event is received.
 ```python
client.AddRequestListener("MyEvent", myEvent.handle)
 ```
