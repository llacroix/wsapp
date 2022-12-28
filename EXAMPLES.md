# Local WebSocket Server

This integration is the most primitive type of websocket server. The WebSocket
is hosted within the application server that handles the connections and the
requests.

With that kind of integration, you're limited to 1 process to host your application.

    python examples/local.py

The websocket should be available on ws://localhost:8000/ws

# Remote Connection WebSocket Server

This integration decouples the WebSocket connections from the WebSocket server. This means
that the WebSocket side of the server doesn't handle the state of connections that didn't
directly connect to the WebSocket server itself. A second service is used to host information
about the WebSocket connections and a way to communicate with the server owning the connection.

With that kind of integration, it is possible to have multiple WebSocket frontend with multiple
connection backend to handle the load. The connection backend could be a database itself but in
this particular example it's a webservice that could have a database backend.

    python example/conn.py # connection server on http://localhost:8004
    python example/remote.py -p 8000 http://localhost:8004
    python example/remote.py -p 8001 http://localhost:8004


To test this properly, you can create a connection to ws://localhost:8000/ws and a second connection
to ws://localhost:8001/ws. Each connections will be stored in the connection server on
http://localhost:8004 .

In this case, the handlers are still local to the websocket server. So the WebSocket server isn't
exactly a "thin" server doing only one thing.

# WebSocket server with remote connections and remote handlers

In this integration, this is the same thing as the previous example. Except that the handlers can
be defined on separated application server. This means, that it's possible to scale the WebSocket
server, the connection server and the application server individually. The big
advantage of this design is that the application server doesn't have to be aware that it is behind
a websocket.

With this kind of implementation, it is possible to create a websocket frontend for servers that do
not support websocket or async in any way. As long as you can create an HTTP Endpoint or possibly 
a message queue... It is possible to add websocket to virtually any kind of application.
