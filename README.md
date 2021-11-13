# pyzmqServer
this is a python client-server connection library built on [pyzmq](https://github.com/zeromq/pyzmq "The python zmq library").
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

to add a request type, you call:
```python
server.AddRequestType("RequestName")
```

now, to make them do something, you have to give them handlers:
```python
server.SetRequestHandler("RequestName", requestHandler)
```
where requestHandler is just a callable function.
if you do it like this, the request are added to the main loop, that updates every second.

you can also create your own loops, that run in their own threads:
```python
server.createEventLoop("RequestLoopName", timeout=1)
server.SetEventHandler("RequestName", requestHandler, "RequestLoopName")
server.eventHandler.startLoop("RequestLoopName")
```
* again, requestHandler is just a `Callable`.
* timeout is the amount of seconds that the loop waits between updates, it defaults to 1.

to start the loop, you need to actually reference the `requestHandler` that the server has, later this will be supported normally.

loops created like this run in a separate thread.
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

#### Requests and Events
the client has a built-in event listener for requests and events that are sent by the server.

to add an event type, you call:
```python
client.AddEventType("EventName")
```

adding a request type is very similar:
```python
client.AddRequestType("RequestName")
```

now, to make them do something, you have to give them handlers:
```python
client.SetEventHandler("EventName", eventHandler)
client.SetRequestHandler("RequestName", requestHandler)
```
where eventHandler and requestHandler are just callable functions.
if you do it like this, the events and request are added to the main loop, that updates every second.

you can also create your own loops, that run in their own threads:
```python
client.createEventLoop("EventLoopName", timeout=1)
client.SetEventHandler("EventName", eventHandler, "EventLoopName")
client.eventHandler.startLoop("EventLoopName")

client.createRequestLoop("RequestLoopName", timeout=1)
client.SetRequestHandler("RequestName", requestHandler, "RequestLoopName")
client.requestHandler.startLoop("RequestLoopName")
```
* again, eventHandler and requestHandler are just `Callable`s.
* timeout is the amount of seconds that the loop waits between updates, it defaults to 1

to start the loop, you need to actually reference the `eventHandler` and `requestHandler` that the client has, later this will be supported normally.

loops created like this run in a separate thread.
I'm thinking about later merging events and requests to run in the same loop.