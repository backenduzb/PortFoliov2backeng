from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi import WebSocket, WebSocketDisconnect
from typing import List
from models.user import User
from models.chat import Global
from permissions import get_current_user_cookie
from authentication.jwt import verify_token
from datetime import datetime
import json
from .chat_schema import GlobalSchema


router = APIRouter(
    prefix='/chat',
    tags=['chat']
)

activate_connections: List[WebSocket] = []

async def connect_user(websocket: WebSocket):
    activate_connections.append(websocket) 

async def disconnect_user(websocket: WebSocket):
    activate_connections.remove(websocket)
    await websocket.close()

async def boardcast_message(message: str):
    for connection in activate_connections:
        await connection.send_text(message) 

@router.get("/global/messages")
async def all_global_messages(
    current_user: User = Depends(get_current_user_cookie)
):
    messages = await Global.all().prefetch_related("user").order_by("id")
    return [
        {
            "content": m.message,
            "sender_id": m.user.id,
            "sender_username": m.user.username,
            "sender_first_name": m.user.first_name,
            "sender_last_name": m.user.last_name,
            "created_at": m.sendet_data
        }
        for m in messages
    ]



@router.websocket("/ws/global")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    token = websocket.cookies.get("access_token")
    if not token:
        await websocket.close(code=1008)
        return

    payload = verify_token(token)
    if not payload:
        await websocket.close(code=1008)
        return

    username = payload.get("sub")
    user = await User.get_or_none(username=username)
    user.is_online=True
    await user.save()
    print(user.is_online)
    if not user:
        await websocket.close(code=1008)
        return

    await connect_user(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            message_data = {
                "content": data,
                "sender_id": user.id,
                "sender_username": user.username,
                "sender_first_name": user.first_name,
                "sender_last_name": user.last_name,
                "created_at": datetime.now().isoformat()
            }
            
            await Global.create(message=message_data["content"],user=user, user_full_name = f"{message_data['sender_first_name']} {message_data['sender_last_name']}", sendet_data = message_data["created_at"], username=message_data["sender_username"])
            await boardcast_message(json.dumps(message_data))

    except WebSocketDisconnect:
        user.is_online=False
        await user.save()
        await disconnect_user(websocket)