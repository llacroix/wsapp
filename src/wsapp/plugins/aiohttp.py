from aiohttp import web
from aiohttp.web import WebSocketResponse
import logging

logger = logging.getLogger(__name__)


class AIOHttpHandler(object):
    def __init__(self, application):
        self.app = application

    def get_ws_handler(self):
        async def websocket_handler(request):
            ws = WebSocketResponse()
            await ws.prepare(request)

            connection = self.app.connection_manager.make_connection(ws)
            await self.app.connection_manager.add_connection(connection)

            # Connect event
            handler = self.app.handler_manager.get('$connect')
            if handler:
                event = self.app.event_manager.make_connect_event(connection)
                await handler(self, event)

            # Messages
            async for msg in ws:
                try:
                    event = self.app.event_manager.make_event(connection, msg)
                    handler = self.app.handler_manager.get_handler(event)
                    if handler:
                        await handler(self, event)
                except Exception as exc:
                    logger.info("Something went wrong", exc_info=True)

                if connection.timed_out:
                    break

            # Disconnect event
            handler = self.app.handler_manager.get('$disconnect')
            if handler:
                event = self.app.event_manager.make_disconnect_event(connection)
                await handler(self, event)

        return websocket_handler

    def connections_handler(self):
        async def connections_handler(request):
            data = await request.json()
            connection_id = request.match_info['connection_id']

            connection = await self.app.connection_manager.get(connection_id)

            if connection:
                # message = self.app.event_manager.make_message(data)

                try:
                    await connection.send(data)
                except Exception as exc:
                    pass

            return web.json_response({})

        return connections_handler

    def add_ws_route(self, webapp):
        webapp.router.add_route(
            'GET',
            '/ws',
            self.get_ws_handler()
        )

    def add_conn_route(self, webapp):
        webapp.router.add_route(
            'POST',
            '/@connections/{connection_id}',
            self.connections_handler()
        )
