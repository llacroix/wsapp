import uuid
from ..objects import Connection

from .base import (
    EndpointManager,
    ConnectionManager
)


class LocalConnection(Connection):

    @property
    def id(self):
        return self.connection_id



class LocalEndpointManager(EndpointManager):
    def __init__(self):
        self.handlers = []
        self.base_handlers = {}

    def get(self, key):
        if key in self.base_handlers:
            return self.base_handlers[key]
        else:
            for name, handler in self.handlers:
                if key == name:
                    return handler

    def add_handler(self, handler, key=None):
        if key in ['$connect', '$disconnect', '$default']:
            self.base_handlers[key] = handler
        else:
            self.handlers.append(handler)

    def get_handler(self, event):
        for key, handler in self.handlers:
            if handler.accept(event):
                event['requestContext']['routeKey'] = key
                return handler
        else:
            event['requestContext']['routeKey'] = '$default'
            return self.base_handlers['$default']


class LocalConnectionManager(ConnectionManager):
    def __init__(self):
        self.connections = {}

    def make_connection(self, socket):
        uuid = self.new_connection_id()
        connection = LocalConnection(socket, connection_id=uuid)
        return connection

    def new_connection_id(self):
        return uuid.uuid1().hex

    async def add_connection(self, connection):
        self.connections[connection.id] = connection

    async def get(self, connection_id):
        return self.connections.get(connection_id)
