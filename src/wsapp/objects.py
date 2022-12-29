import time


class Connection(object):
    """
    A Connection object provides a simple interface to communicate
    with a client. The socket object must implement a single
    method named `send_json`.

    The communication with the socket is always unilateral and the
    data received from the endpoint can be ignored.
    """
    def __init__(
            self,
            socket,
            connection_id=None,
            timeout=1*60,
            connected_at=None
    ):
        self.id = connection_id
        self.socket = socket

        if connected_at is None:
            # TODO use an actual date
            self.connected_at = time.perf_counter()
        else:
            self.connected_at = connected_at

        self.timeout = timeout

    @property
    def timed_out(self):
        # TODO use an actual date
        cur_time = time.perf_counter()
        return (cur_time - self.connected_at) > self.timeout

    def get_info(self):
        return {
            "id": self.id,
            "connected_at": self.connected_at,
        }

    async def send(self, message):
        return await self.socket.send_json(message)
