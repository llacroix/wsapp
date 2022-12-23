import click
import aiohttp
from aiohttp import web, ClientSession
import logging

logger = logging.getLogger(__name__)


async def make_service(http_endpoint):
    connections = {}

    session = ClientSession()

    routes = web.RouteTableDef()

    @routes.get('/@connections/{connection_id}')
    async def get_connection_info(request):
        connection_id = request.match_info['connection_id']
        info = connections.get(connection_id)
        return web.json_response(info)

    @routes.post('/@connections/{connection_id}')
    async def post_connection_message(request):
        connection_id = request.match_info['connection_id']
        info = connections.get(connection_id)

        message = await request.json()

        host_url = info['host']
        url = f"{host_url}/@connections/{connection_id}"

        async with session.post(url, json=message) as resp:
            await resp.json()

        return web.json_response({})

    @routes.post('/@connections')
    async def new_connection(request):
        data = await request.json()

        logger.info(data)

        if 'id' in data:
            connections[data['id']] = data

        return web.json_response({})

    return routes


async def make_application(http_endpoint):
    routes = await make_service(http_endpoint)

    webapp = aiohttp.web.Application()

    webapp.router.add_routes(routes)

    return webapp


@click.command()
@click.option('--host', help="Listen Hostname", default='127.0.0.1')
@click.option('--port', help="Listen Hostname", default=8004, type=int)
def main(host, port):
    logging.basicConfig(level='INFO')

    http_endpoint = f"http://{host}:{port}"

    aiohttp.web.run_app(
        make_application(http_endpoint),
        host=host,
        port=port
    )

if __name__ == '__main__':
    main()
