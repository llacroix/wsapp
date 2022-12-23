import time


class BaseManager(object):
    def __init__(self, app=None):
        self.app = app

    def register(self, app):
        self.app = app

class ConnectionManager(object):

    async def add_connection(self, connection):
        raise NotImplementedError()

    def new_connection_id(self):
        raise NotImplementedError()

    async def get(self, connection_id):
        raise NotImplementedError()


class EventManager(object):
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
            event['requestContext']['routeKey'] = '$connect'
        return event

    def make_connect_event(self, connection):
        event = self.make_default_event(
            connection,
            route_key='$connect'
        )
        return event

    def make_event(self, connection, message, route_key=None):
        event = self.make_default_event(
            connection,
            route_key=route_key
        )
        event['body'] = message.json()
        return event

    def make_disconnect_event(self, connection):
        event = self.make_default_event(
            connection,
            route_key='$disconnect'
        )
        return event


class EndpointManager(object):
    def add_handler(self, handler, key=None):
        raise NotImplementedError()

    def get_handler(self, event):
        raise NotImplementedError()

    def define(self, key):
        def decorator(handler):
            self.add_handler(handler, key)
            return handler
        return decorator
