# pyzmqServer
this is a python client-server connection library built on pyzmq.
## usage
### server side
to use the server, you have to import the 'Server' class from 'pyzmqServer.server'.

#### initialization

creating a server has three arguments.
* eventPort - the port where the clients can listen for server events.
* replyPort - the port where the server listens for requests from clients and .replys to them.
* clientType - the type the server uses to store a client.
    - default - 'pyzmqServer.server.ClientConnection'.
``` python
from pyzmqServer.server import Server

eventSendPort = 5555
requestRecvReplyPort = 5556

conn = Server(eventSendPort, requestRecvReplyPort)
```
### client side
to use the client, you need to import the 'Client' class from 'pyzmqServer.client'.
#### initialization
creating a client has five arguments:
* clientIp - the IP address of the client as a string.
* serverIp - the IP address of the server as a string.
* eventPort - the port on the server where the client listens for server events.
* requestSendPort - the port on the server listens to which the client can send a request.
* requestReceivePort - the port where the client listens for requests send from the server.
``` python
from pyzmqServer.client import Client

clientIp = "127.0.0.1"
serverIp = "127.0.0.1"
eventRecvPort = 5555
requestSendPort = 5556
requestRecvReplyPort = 5557

conn = Server(eventRecvPort, requestSendPort, requestRecvReplyPort)
```