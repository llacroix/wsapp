import time


class BaseManager(object):
    def __init__(self, app=None):
        self.app = app

    def register(self, app):
        self.app = app


class ConnectionManager(object):
    """
    An abstract class defining basic methods that needs
    to be implemented by a connection manager.

    A Connection manager is a special database that can create
    connection object and put connection object in a database
    to be used by the current websocket application.

    Here's the life cycle of a connection owned by the websocket
    service.

    1. A client is connected and a connection is created through:
       make_connection.

    2. The new connection is then added to the connection manager
       through `add(conn_id)`.

    3. If the socket connection lives longer than the timeout. It will
       automatically stop waiting for messages and close the socket.

    4. After the websocket is closed, the connection gets removed
       from the connection manager with `remove(conn_id)`


    At any point, a connection can be obtained using the `get(conn_id)`
    method. Depending on the implementation, the connection returned
    could be a local connection or a connection stored somewhere else.
    """

    def make_connection(self, websocket):
        """
        Creates a connection object
        """
        raise NotImplementedError()

    async def add(self, connection):
        raise NotImplementedError()

    async def get(self, connection_id):
        raise NotImplementedError()

    async def remove(self, connection):
        raise NotImplementedError()


class DictAttr(dict):
    def __getattr__(self, name):
        try:
            val = self[name]
        except KeyError:
            raise AttributeError(f"Attribute {name} not found")

        if isinstance(val, dict):
            return DictAttr(val)
        else:
            return val


class EventManager(object):
    """
    A structure that has for purpose to create Event object relevant
    to the circumstances. There are default events that aren't based
    on data received.

    Connected Event:

    This type of event may contain information based on the data
    received in the http request that created the connection.

    Other Events / Default:

    These events are based on the data received from the client and
    the route being used to handle the event.

    Disconnect Event:

    This type of event isn't based on any message received and at this
    point. The connection is no longer active. This can be used for cleaning
    up things.
    """
    def __init__(self, route_expression):
        self.route_expression = route_expression

    def make_default_event(self, connection, route_key=None):
        event = {
            "requestContext": {
                "connectionId": connection.id,
                "connectedAt": connection.connected_at,
                "requestTimeEpoch": time.perf_counter()
            },
            "body": {}
        }

        if route_key is not None:
            event['requestContext']['routeKey'] = route_key

        return DictAttr(event)

    def make_connect_event(self, request, connection):
        event = self.make_default_event(
            connection,
            route_key='$connect'
        )
        return DictAttr(event)

    def compute_route_key(self, event):
        try:
            route_key = self.route_expression.format(request=event)
        except AttributeError:
            route_key = "$default"

        return route_key

    def make_event(self, connection, message, route_key=None):
        event = self.make_default_event(
            connection,
            route_key=route_key
        )
        event['body'] = message.json()

        event['requestContext']['routeKey'] = self.compute_route_key(event)

        return DictAttr(event)

    def make_disconnect_event(self, connection):
        event = self.make_default_event(
            connection,
            route_key='$disconnect'
        )
        return DictAttr(event)


class HandlerManager(object):

    def __init__(self, route_expression=None):
        self.handlers = {}
        self.base_handlers = {}
        self.route_expression = route_expression

    def get(self, key):
        if key in self.base_handlers:
            return self.base_handlers[key]
        else:
            for name, handler in self.handlers.items():
                if key == name:
                    return handler

    def add_handler(self, handler, key=None):
        if key is None:
            key = handler.name

        if key in ['$connect', '$disconnect', '$default']:
            self.base_handlers[handler.name] = handler
        else:
            self.handlers[handler.name] = handler

    def add_handlers(self, handler_map):
        for key, handler in handler_map.items():
            self.add_handler(handler)

    def get_handler(self, event):
        route_key = event['requestContext']['routeKey']

        handler = (
            self.handlers.get(route_key)
            if route_key in self.handlers
            else self.base_handlers.get('$default')
        )

        return handler
