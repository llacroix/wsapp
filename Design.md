# How It Works

WebSockets is generally not used because it's claimed too not scale well and
sometimes it's even difficult to integrate because a WebSocket server is likely to
run in greenthreads or async jobs. This involve making specific design choices
while developping your software. Sometimes, WebSocket is simply completely
incompatible with your stack and it would feel like there's nothing you can do
about it.

This librarie attempt to provide the basic tools to design a scalable websocket
server that does mainly this.

The main difference is that application server often attempt to be an http server
and a websocket server all in one. This project aim to remote the websocket specific
code from your application by providing an interface that can be slightly integrated
or completely separated by using http or some other way to communicate with backends.

When a client connect to a websocket, it would connect to the websocket server:

    Client -> WebSocketServer

Then the WebSocketServer would have to create a Connection object that keep tracks
of users connected to the WebSocket server or potentially a cluster. 

When the connection object is created, it is then possible to dispatch a first event
to a backend as defined.

   Client -> WebSocketServer
              -> Create Connection
              -> Connect Event

Ideally, your application would have to initialize a session for a user at this point
and prepare the session of the user somewhere. When this is done, the server is going
to wait for events from the websocket endpoint.

   
   Client -> WebSocketServer
              -> Create Connection
              -> Connect Event
              -> Process Messages


This is similar to processing http requests. But the difference is that events always come
from the client and a connection server would be responsible for dispatching messages to
the websocket client.

When the connection times out or if the connection is lost, the Disconnect event is triggered.


   Client -> WebSocketServer
              -> Create Connection
              -> Connect Event
              -> Process Messages
              -> Disconnect Event


This part can be used to cleanup things that were done in the first connect event. As you can see
none of this allows you to send messages to websocket clients. And the reason for this is
that it's easier to work with websockets when we don't mix up sending messages and receiving them.

For that, there is the connection server. And what's particularly great about the connection server
is that anything outside of websocket can be used to send messages to clients. When developping 
your application, you don't have to have a direct access to a websocket. The connection server
exists to dispatch the messages wherever it needs and the application only have to know
how to communicate with the connection server.


Sending a message back to WebSocket can be summed as this:

    HttpClient -> ConnectionServer (connection_id)
                    -> Send Message to WebSocket Server with the connection
                       -> WebSocket send message through websocket

You could technically send messages to websocket from anywhere that can access the connection server.
