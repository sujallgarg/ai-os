from fastapi import (
    WebSocket
)


class ConnectionManager:

    def __init__(self):

        self.connections: dict[
            str,
            set[WebSocket]
        ] = {}

    async def connect(
        self,
        user_id: str,
        websocket: WebSocket
    ):

        await websocket.accept()

        if user_id not in self.connections:

            self.connections[user_id] = set()

        self.connections[
            user_id
        ].add(websocket)


    def disconnect(
        self,
        user_id: str,
        websocket: WebSocket
    ):

        connections = (
            self.connections.get(
                user_id
            )
        )

        if not connections:
            return

        connections.discard(
            websocket
        )

        if not connections:

            self.connections.pop(
                user_id,
                None
            )


    async def send_to_user(
        self,
        user_id: str,
        event: dict
    ):

        connections = (
            self.connections.get(
                user_id,
                set()
            )
        )

        dead = []

        for websocket in connections:

            try:

                await websocket.send_json(
                    event
                )

            except Exception:

                dead.append(
                    websocket
                )

        for websocket in dead:

            self.disconnect(
                user_id,
                websocket
            )


    async def broadcast(
        self,
        event: dict
    ):

        for user_id in list(
            self.connections.keys()
        ):

            await self.send_to_user(
                user_id,
                event
            )


websocket_manager = (
    ConnectionManager()
)