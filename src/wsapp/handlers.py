import inspect
from typing import Callable, Any


class Handler(object):
    def __init__(self, name):
        self.name = name

    def call(self, application, event):
        raise NotImplementedError()


class HandlerMap(object):
    pass


class BasicHandler(Handler):
    def __init__(self, name: str, func: Callable[[Any, Any], None]):
        super().__init__(name)
        self.func = func

    async def call(self, application, event):
        res = self.func(application, event)

        if inspect.isawaitable(res):
            return await res

        return res


class BasicHandlerMap(HandlerMap):
    def __init__(self):
        self.handlers = {}

    def define(self, key):
        def decorator(handler):
            def_handler = BasicHandler(key, handler)
            self.handlers[def_handler.name] = def_handler
            return handler
        return decorator

    def items(self):
        return self.handlers.items()


class HttpEndpoint(object):
    def __init__(self, url, session):
        self.url = url
        self.session = session

    async def send(self, path, event):
        url = f"{self.url}{path}"

        async with self.session.post(url, json=event) as req:
            result = await req.json()

        return result


class HttpHandler(Handler):
    def __init__(self, name: str, endpoint: HttpEndpoint, path: str):
        super().__init__(name)
        self.endpoint = endpoint
        self.path = path

    async def call(self, application, event):
        await self.endpoint.send(self.path, event)


class HttpHandlerMap(HandlerMap):
    def __init__(self, endpoint: HttpEndpoint):
        self.endpoint = endpoint
        self.handlers = {}

    def define(self, name, path):
        handler = HttpHandler(name, self.endpoint, path)
        self.handlers[handler.name] = handler
        return handler

    def add(self, handler: HttpHandler):
        self.handlers[handler.name] = handler

    def items(self):
        return self.handlers.items()
