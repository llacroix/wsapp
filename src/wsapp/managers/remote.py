from .base import ConnectionManager
from .local import LocalConnectionManager
from ..objects import Connection


class ConnectionEndpoint(object):
    """
    ConnectionEndpoint is used to communicate with a connection server. This
    is a basic client without any kind of authentication process.
    """
    def __init__(self, ws_url, url, session):
        self.session = session
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

    async def remove_connection(self, connection):
        url = f"{self.url}/@connections/{connection.id}"

        async with self.session.delete(url) as resp:
            info = await resp.json()

        return info


class RemoteSocket(object):
    """
    Socket object that mimmick an object that can send_json
    to some destination.

    This particular socket is used to send json to an
    http endpoint based on a specific connection id.
    """
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

    async def add(self, connection):
        # Do not add remote connections to local connections
        if not isinstance(connection, RemoteConnection):
            await super().add(connection)
            await self.remote_endpoint.add_connection(connection)

    async def get(self, connection_id):
        if connection_id in self.connections:
            return await super().get(connection_id)
        else:
            connection = await self.remote_endpoint.get_connection(
                connection_id
            )

            # TODO add to a cache that purge itself overtime
            if connection.id not in self.remote_connections:
                self.remote_connections[connection.id] = connection

            return connection

    async def remove(self, connection):
        is_local = connection.id in self.connections

        await super().remove(connection)

        if is_local:
            await self.remote_endpoint.remove_connection(connection)
        else:
            del self.remote_connections[connection.id]
