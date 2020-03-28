from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.routers import players, decks, games
from peewee import SqliteDatabase
from app import models

db = SqliteDatabase('condottiere.db')

db.create_tables([models.Player, models.Card, models.Deck, models.Game])

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    players.router,
    prefix="/players",
)

app.include_router(
    decks.router,
    prefix="/decks",
)

app.include_router(
    games.router,
    prefix="/games",
)

clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for client in clients:
                print('   ', client)
                await client.send_text(data)
    except WebSocketDisconnect:
        clients.remove(websocket)
