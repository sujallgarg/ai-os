"""
Event Manager.
Emits system events and broadcasts them to connected WebSocket clients.
"""

from events.models import SystemEvent
from api.websocket import websocket_manager


class EventManager:

    async def emit(
        self,
        event: SystemEvent,
        user_id: str = "development-user"
    ):
        """
        Broadcast a system event via WebSocket.
        """
        payload = event.to_dict()
        try:
            await websocket_manager.broadcast(payload)
        except Exception as err:
            print(f"[EventManager] Broadcast error: {err}")


event_manager = EventManager()
