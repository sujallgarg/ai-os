from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect
)

from api.websocket import (
    websocket_manager
)


router = APIRouter()


@router.websocket(
    "/ws"
)
async def websocket_endpoint(
    websocket: WebSocket
):

    # ------------------------------------------------------------
    # DEVELOPMENT USER
    # ------------------------------------------------------------

    # Replace this with your authenticated
    # user ID in Step 90.

    user_id = "development-user"

    await websocket_manager.connect(
        user_id,
        websocket
    )

    try:

        await websocket.send_json({

            "event":
                "connection.established",

            "data": {
                "message":
                    "Real-time connection established."
            }
        })


        while True:

            # Keep connection alive.

            await websocket.receive_text()

    except WebSocketDisconnect:

        websocket_manager.disconnect(
            user_id,
            websocket
        )

    except Exception:

        websocket_manager.disconnect(
            user_id,
            websocket
        )