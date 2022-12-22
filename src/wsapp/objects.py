import time


class Connection(object):
    def __init__(self, socket, timeout=1*60):
        self.socket = socket
        self.connected_at = time.perf_counter()
        self.timeout = timeout

    @property
    def id(self):
        raise NotImplementedError()

    @property
    def timed_out(self):
        cur_time = time.perf_counter()
        return (cur_time - self.connected_at) > self.timeout

    async def send(self, message):
        return await self.socket.send_json(message)

