import uuid
from ..objects import Connection
from .base import ConnectionManager


class LocalConnection(Connection):
    pass


class LocalConnectionManager(ConnectionManager):
    def __init__(self):
        self.connections = {}

    def make_connection(self, socket):
        return LocalConnection(socket)

    def new_connection_id(self):
        return uuid.uuid1().hex

    async def add_connection(self, connection):
        connection.id = self.new_connection_id()
        self.connections[connection.id] = connection

    async def get(self, connection_id):
        return self.connections.get(connection_id)

    async def remove(self, connection):
        if connection.id in self.connections:
            del self.connections[connection.id]
