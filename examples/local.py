import click
import logging
import aiohttp

from wsapp.managers.base import EventManager, HandlerManager
from wsapp.handlers import BasicHandlerMap
from wsapp.managers.local import (
    LocalConnectionManager,
)
from wsapp.app import WebsocketApplication
from wsapp.plugins.aiohttp import AIOHttpHandler


logger = logging.getLogger(__name__)


async def make_service():
    handler_map = BasicHandlerMap()

    @handler_map.define('$connect')
    async def connect(app, event):
        logger.info("On connect %s", event)

    @handler_map.define("$disconnect")
    async def disconnect(app, event):
        logger.info("On Disconnect %s", event)

    @handler_map.define("$default")
    async def default_handler(app, event):
        logger.info("On Default %s", event)
        conn = await connections.get(event['requestContext']['connectionId'])
        logger.info("Connection %s", conn)
        await conn.send(event['body'])

    @handler_map.define("action-fun")
    async def fun_action(app, event):
        logger.info("On Fun %s", event)

    handlers = HandlerManager()
    events = EventManager("action-{request.body.action}")
    connections = LocalConnectionManager()
    handlers.add_handlers(handler_map)

    application = WebsocketApplication(connections, handlers, events)
    return application


async def make_application(ws_endpoint):
    application = await make_service()

    webapp = aiohttp.web.Application()
    wsapp = AIOHttpHandler(application)
    wsapp.add_ws_route(webapp)
    wsapp.add_conn_route(webapp)

    return webapp


@click.command()
@click.option('--host', help="Listen Hostname", default='127.0.0.1')
@click.option('--port', help="Listen Hostname", default=8000, type=int)
def main(host, port):
    logging.basicConfig(level='INFO')

    ws_endpoint = f"http://{host}:{port}"

    aiohttp.web.run_app(
        make_application(ws_endpoint),
        host=host,
        port=port
    )


if __name__ == '__main__':
    main()
