from .managers.base import (
    ConnectionManager,
    HandlerManager,
    EventManager
)


class WebsocketApplication(object):
    def __init__(
        self,
        connection_manager: ConnectionManager,
        handler_manager: HandlerManager,
        event_manager: EventManager
    ):
        self.connection_manager = connection_manager
        self.handler_manager = handler_manager
        self.event_manager = event_manager
