from typing import Callable

class EventSystem:
    def __init__(self):
        self._event_handlers = {}

    def on_call(self, event_name: str):
        def decorator(func: Callable):
            if event_name not in self._event_handlers:
                self._event_handlers[event_name] = []
            self._event_handlers[event_name].append(func)
            return func
        return decorator

    async def call(self, event_name: str, *args, **kwargs):
        if event_name in self._event_handlers:
            for handler in self._event_handlers[event_name]:
                await handler(*args, **kwargs)

events = EventSystem()

# == events ==
RPC_UPDATED = "rpc_updated"
AVATAR_UPDATED = "avatar_updated"