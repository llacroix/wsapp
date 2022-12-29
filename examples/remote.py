import click
import logging
import aiohttp

from wsapp.managers.base import EventManager
from wsapp.handlers import BasicHandlerMap
from wsapp.managers.base import HandlerManager
from wsapp.managers.remote import (
    RemotedConnectionManager,
    ConnectionEndpoint
)
from wsapp.app import WebsocketApplication

from wsapp.plugins.aiohttp import AIOHttpHandler


logger = logging.getLogger(__name__)


async def make_service(ws_endpoint, remote_connections):
    session = aiohttp.ClientSession()
    conn_endpoint = ConnectionEndpoint(
        ws_endpoint,
        remote_connections,
        session
    )
    connections = RemotedConnectionManager(conn_endpoint)

    handler_map = BasicHandlerMap()

    @handler_map.define('$connect')
    async def connect(app, event):
        logger.info("On connect %s", event)

    @handler_map.define("$disconnect")
    async def disconnect(app, event):
        logger.info("On Disconnect %s", event)

    @handler_map.define("$default")
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

        logger.info(
            "Default handler with Connection %s on Event: %s", conn, event
        )

    @handler_map.define("action-fun")
    async def action_fun(app, event):
        logger.info("In app fun")

    handlers = HandlerManager()
    handlers.add_handlers(handler_map)

    events = EventManager("action-{request.body.action}")

    application = WebsocketApplication(connections, handlers, events)

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
