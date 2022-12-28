import uuid
from ..objects import Connection
from .base import ConnectionManager


class LocalConnection(Connection):

    @property
    def id(self):
        return self.connection_id


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
