from aiohttp import web
from aiohttp.web import WebSocketResponse
import logging

logger = logging.getLogger(__name__)


class AIOHttpHandler(object):
    def __init__(self, application):
        self.app = application

    def get_ws_handler(self):
        """
        Define main websocket loop for aiohttp server.
        """
        async def websocket_handler(request):
            ws = WebSocketResponse()
            await ws.prepare(request)

            connection = self.app.connection_manager.make_connection(ws)
            await self.app.connection_manager.add(connection)

            # Connect event
            handler = self.app.handler_manager.get('$connect')
            if handler:
                event = self.app.event_manager.make_connect_event(
                    request,
                    connection
                )
                await handler.call(self, event)

            # TODO break out of the loop when timeout is reached.
            # Messages
            async for msg in ws:
                event = self.app.event_manager.make_event(connection, msg)

                handler = self.app.handler_manager.get_handler(event)
                if handler:
                    await handler.call(self, event)

                # lazy way to expire a socket
                if connection.timed_out:
                    break

            # Disconnect event
            handler = self.app.handler_manager.get('$disconnect')
            if handler:
                event = self.app.event_manager.make_disconnect_event(
                    connection
                )
                await handler.call(self, event)

            await self.app.connection_manager.remove(connection)

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
                except Exception:
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
