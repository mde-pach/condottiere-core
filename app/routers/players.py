from fastapi import APIRouter, Header, HTTPException, WebSocket
from pydantic import BaseModel
from app import models
import random
import string

router = APIRouter()


class Player(BaseModel):
    name: str

class Card(BaseModel):
    board: bool = None
    belongs_to_player: bool = True

@router.get("")
def get_players():
    return [
        {
            'name': player.name,
            'id': player.id,
            'board': [card.serialize() for card in player.cards.where(models.Card.board == True)]
        } for player in models.Player.select()
    ]

@router.post("")
def create_player(player_to_create: Player):
    player = models.Player(name=player_to_create.name, secret=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25)))
    player.save()
    return player.serialize()

@router.get("/me")
def get_current_player(x_secret_token: str = Header(None)):
    try:
        player = models.Player.get(secret=x_secret_token)
        return {
            'name': player.name,
            'id': player.id,
            'hand': [card.serialize() for card in player.cards.where(models.Card.board == False)],
            'board': [card.serialize() for card in player.cards.where(models.Card.board == True)]
        }
    except:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

@router.get("/{player_id}")
def get_players(player_id: int):
    player = models.Player.get(player_id)
    return {
        'name': player.name,
        'id': player.id,
        'board': [card.serialize() for card in player.cards.where(models.Card.board == True)]
    }

@router.delete("/{player_id}")
def delete_player(player_id: int, x_secret_token: str = Header(None)):
    player = models.Player.get(player_id)
    for card in player.cards:
        card.player = None
        card.board = False
        card.save()
    player.delete().where(models.Player.id == player_id).execute()
    return 200

@router.patch("/{player_id}/cards/{card_id}")
def update_player_card(player_id: int, card_id: int, patch_to_card: Card, x_secret_token: str = Header(None)):
    player = models.Player.get(player_id)
    if x_secret_token == player.secret:
        card = models.Player.get(player_id).cards.where(models.Card.id == card_id).get()
        if patch_to_card.board is not None:
            card.board = patch_to_card.board
        if patch_to_card.belongs_to_player is False:
            card.player = None
            card.board = False
        card.save()
        return card.serialize()
    else:
        raise HTTPException(
            status_code=403,
            detail="Player token incorrect"
        )

