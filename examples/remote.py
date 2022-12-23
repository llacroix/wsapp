import click
import logging
import aiohttp

from wsapp.managers.base import EventManager
from wsapp.managers.local import (
    LocalConnectionManager,
    LocalEndpointManager
)
from wsapp.managers.remote import (
    RemotedConnectionManager,
    ConnectionEndpoint
)
from wsapp.app import WebsocketApplication

from wsapp.plugins.aiohttp import AIOHttpHandler


logger = logging.getLogger(__name__)


async def make_service(ws_endpoint, remote_connections):
    conn_endpoint = ConnectionEndpoint(ws_endpoint, remote_connections)

    handlers = LocalEndpointManager()
    events = EventManager()
    connections = RemotedConnectionManager(conn_endpoint)

    application = WebsocketApplication(connections, handlers, events)

    @handlers.define('$connect')
    async def connect(app, event):
        logger.info("On connect %s", event)


    @handlers.define("$disconnect")
    async def disconnect(app, event):
        logger.info("On Disconnect %s", event)


    @handlers.define("$default")
    async def default_handler(app, event):
        if 'connectionId' in event['body']:
            # Attempt to send a message to a specified connection id
            connection_id = event['body']['connectionId']
        else:
            connection_id = event['requestContext']['connectionId']

        # Connection can be either local or remote but works transparently
        conn = await connections.get(connection_id)
        if conn:
            await conn.send(event['body'])

        logger.info("Default handler with Connection %s on Event: %s", conn, event)

    return application


async def make_application(ws_endpoint, remote_endpoint):
    application = await make_service(ws_endpoint, remote_endpoint)

    webapp = aiohttp.web.Application()
    wsapp = AIOHttpHandler(application)
    wsapp.add_ws_route(webapp)
    wsapp.add_conn_route(webapp)

    return webapp


@click.command()
@click.argument('remote_endpoint')
@click.option('--host', help="Listen Hostname", default='127.0.0.1')
@click.option('--port', help="Listen Hostname", default=8000, type=int)
def main(remote_endpoint, host, port):
    logging.basicConfig(level='INFO')

    ws_endpoint = f"http://{host}:{port}"

    aiohttp.web.run_app(
        make_application(ws_endpoint, remote_endpoint),
        host=host,
        port=port
    )

if __name__ == '__main__':
    main()
