import click
import logging
import aiohttp

from wsapp.managers.base import EventManager
from wsapp.handlers import HttpHandlerMap
from wsapp.managers.base import HandlerManager
from wsapp.managers.remote import (
    RemotedConnectionManager,
    ConnectionEndpoint
)
from wsapp.app import WebsocketApplication

from wsapp.plugins.aiohttp import AIOHttpHandler


logger = logging.getLogger(__name__)


async def make_service(ws_endpoint, remote_endpoint):
    session = aiohttp.ClientSession()
    conn_endpoint = ConnectionEndpoint(
        ws_endpoint,
        remote_endpoint,
        session
    )

    connections = RemotedConnectionManager(conn_endpoint)

    handler_map = HttpHandlerMap(remote_endpoint, session)

    handler_map.define("$connect", "/httpws/connect")
    handler_map.define("$disconnect", "/httpws/disconnect")
    handler_map.define("$default", "/httpws/default")
    # handler_map.define("action.fun", "/httpws/fun")

    handlers = HandlerManager()
    handlers.add_handlers(handler_map)

    events = EventManager()

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
