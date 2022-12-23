import logging
import aiohttp

from wsapp.managers.base import EventManager
from wsapp.managers.local import (
    LocalConnectionManager,
    LocalEndpointManager
)
from wsapp.app import WebsocketApplication

from wsapp.plugins.aiohttp import AIOHttpHandler


logging.basicConfig(level='INFO')

logger = logging.getLogger(__name__)

handlers = LocalEndpointManager()
events = EventManager()
connections = LocalConnectionManager()

application = WebsocketApplication(connections, handlers, events)

@handlers.define('$connect')
async def connect(app, event):
    logger.info("On connect %s", event)


@handlers.define("$disconnect")
async def disconnect(app, event):
    logger.info("On Disconnect %s", event)


@handlers.define("$default")
async def default_handler(app, event):
    logger.info("On Default %s", event)
    conn = await connections.get(event['requestContext']['connectionId'])
    logger.info("Connection %s", conn)
    await conn.send(event['body'])


webapp = aiohttp.web.Application()

wsapp = AIOHttpHandler(application)

wsapp.add_ws_route(webapp)
wsapp.add_conn_route(webapp)

aiohttp.web.run_app(webapp, host='localhost', port=8000)
