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
        if self.route_expression:
            route_key = self.route_expression.format(request=event)
            if route_key in self.handlers:
                event['requestContext']['routeKey'] = route_key
                return self.handlers[route_key]

        for key, handler in self.handlers.items():
            if handler.accept(event):
                event['requestContext']['routeKey'] = key
                return handler
        else:
            event['requestContext']['routeKey'] = '$default'
            return self.base_handlers['$default']
