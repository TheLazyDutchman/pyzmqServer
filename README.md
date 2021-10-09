# pyzmqServer
this is a python client-server connection library built on pyzmq
## usage
### server
to use the server, you have to import the 'Server' class from 'pyzmq.server'

#### creation

creating a server has three arguments
*eventPort - the port where the clients can listen for server events
*replyPort - the port where the server listens for requests from clients and replys to them
*clientType - the type the server uses to store a client
    default - 'pyzmqServer.server.ClientConnection'
``` python
from pyzmq.server import Server

eventRecvPort = 5555
requestRecvReplyPort = 5556

conn = Server(evenRecvPort, requestRecvReplyPort)
```