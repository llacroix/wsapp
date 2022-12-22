class WebsocketApplication(object):
    def __init__(self, connection_manager, handler_manager, event_manager):
        self.connection_manager = connection_manager
        self.handler_manager = handler_manager
        self.event_manager = event_manager
