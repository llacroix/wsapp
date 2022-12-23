import time


class Connection(object):
    def __init__(self, socket, connection_id=None, timeout=1*60, connected_at=None):
        self.socket = socket

        self.connection_id = connection_id

        if connected_at is None:
            self.connected_at = time.perf_counter()
        else:
            self.connected_at = connected_at

        self.timeout = timeout

    @property
    def id(self):
        return self.connection_id

    @property
    def timed_out(self):
        cur_time = time.perf_counter()
        return (cur_time - self.connected_at) > self.timeout

    async def send(self, message):
        return await self.socket.send_json(message)


    def get_info(self):
        return {
            "id": self.id,
            "connected_at": self.connected_at,
        }
