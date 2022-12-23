from aiohttp import ClientSession
from .base import EndpointManager, ConnectionManager
from .local import LocalConnectionManager
from ..objects import Connection


class ConnectionEndpoint(object):
    def __init__(self, ws_url, url, session_constructor=ClientSession):
        self.session = session_constructor()
        self.ws_url = ws_url
        self.url = url

    async def send_json(self, connection_id, message):
        url = f"{self.url}/@connections/{connection_id}"
        async with self.session.post(url, json=message) as resp:
            await resp.json()

    async def get_connection(self, connection_id):
        url = f"{self.url}/@connections/{connection_id}"

        async with self.session.get(url) as resp:
            info = await resp.json()

        socket = RemoteSocket(connection_id, self)

        conn = RemoteConnection(
            socket,
            connection_id=connection_id,
            timeout=info.get('timeout'),
            connected_at=info.get('connected_at')
        )

        return conn

    async def add_connection(self, connection):
        message = connection.get_info()

        message['host'] = self.ws_url

        url = f"{self.url}/@connections"

        async with self.session.post(url, json=message) as resp:
            await resp.json()


class RemoteSocket(object):
    def __init__(self, connection_id, endpoint):
        self.connection_id = connection_id
        self.endpoint = endpoint

    async def send_json(self, message):
        await self.endpoint.send_json(
            self.connection_id,
            message
        )


class RemoteConnection(Connection):
    pass


class RemotedConnectionManager(LocalConnectionManager):
    def __init__(self, remote_endpoint):
        super().__init__()
        self.remote_endpoint = remote_endpoint
        self.remote_connections = {}

    async def add_connection(self, connection):
        # Do not add remote connections to local connections
        if not isinstance(connection, RemoteConnection):
            await super().add_connection(connection)
            await self.remote_endpoint.add_connection(connection)

    async def get(self, connection_id):
        if connection_id in self.connections:
            return await super().get(connection_id)
        else:
            connection = await self.remote_endpoint.get_connection(connection_id)

            # TODO add to a cache that purge itself overtime
            if connection.id not in self.remote_connections:
                self.remote_connections[connection.id] = connection

            return connection
