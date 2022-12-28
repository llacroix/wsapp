import inspect


class Handler(object):
    def __init__(self, name):
        self.name = name

    def call(self, application, event):
        raise NotImplementedError()

    def accept(self, event):
        raise NotImplementedError()


class BasicHandler(Handler):
    def __init__(self, name, func):
        super().__init__(name)
        self.func = func

    async def call(self, application, event):
        res = self.func(application, event)

        if inspect.isawaitable(res):
            return await res

        return res

    def accept(self, event):
        return True


class BasicHandlerMap(object):
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


class HttpHandler(Handler):
    def __init__(self, name, endpoint, path):
        super().__init__(name)
        self.endpoint = endpoint
        self.path = path

    async def call(self, application, event):
        await self.endpoint.send(self.path, event)


class HttpEndpointMap(object):
    def __init__(self, url, session):
        self.url = url
        self.session = session
        self.handlers = {}

    async def send(self, path, event):
        url = f"{self.url}{path}"

        async with self.session.post(url, json=event.to_json()) as req:
            result = await req.json()

        return result

    def define(self, name, path):
        handler = HttpHandler(name, self, path)
        self.handlers[handler.name] = handler
        return handler
