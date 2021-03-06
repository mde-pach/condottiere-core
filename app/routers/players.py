from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from app import models
import random
import string
import itertools

router = APIRouter()


class Player(BaseModel):
    name: str = None
    game_id: int = None
    money: int = None

class Card(BaseModel):
    board: bool = None
    belongs_to_player: bool = True
    discarded: bool = True
    player_id: int = None

@router.get("")
def get_players():
    return [
        {
            'name': player.name,
            'id': player.id,
            'board': [card.serialize() for card in player.cards.where(models.Card.board == True).order_by(models.Card.view_order)],
            'game_id': player.game_id
        } for player in models.Player.select()
    ]

@router.post("")
def create_player(player_to_create: Player):
    player = models.Player(name=player_to_create.name, secret=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25)))
    player.save()
    return {
        'name': player.name,
        'id': player.id,
        'secret': player.secret
    }

@router.patch("/{player_id}")
def update_player(player_id: int, player: Player, x_secret_token: str = Header(None)):
    player_to_update = models.Player.get(player_id)
    if player.name is not None:
        player_to_update.name = player.name
    if player.money is not None:
        player_to_update.money = player.money
    if player.game_id is not None:
        player_to_update.game_id = player.game_id
    player_to_update.save()
    return 200

@router.get("/me")
def get_current_player(x_secret_token: str = Header(None)):
    try:
        player = models.Player.get(secret=x_secret_token)
        return {
            'name': player.name,
            'id': player.id,
            'money': player.money,
            'hand': [card.serialize() for card in player.cards.where(models.Card.board == False).where(models.Card.deck << models.Deck.select().where(models.Deck.game_id == player.game_id)).order_by(models.Card.view_order)],
            'board': [card.serialize() for card in player.cards.where(models.Card.board == True).where(models.Card.deck << models.Deck.select().where(models.Deck.game_id == player.game_id)).order_by(models.Card.view_order)],
            'game_id': player.game_id
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
        'money': player.money,
        'board': [card.serialize() for card in player.cards.where(models.Card.board == True).where(models.Card.deck << models.Deck.select().where(models.Deck.game_id == player.game_id)).order_by(models.Card.view_order)],
        'game_id': player.game_id
    }

@router.delete("/{player_id}")
def delete_player(player_id: int, x_secret_token: str = Header(None)):
    player = models.Player.get(player_id)
    for card in player.cards:
        card.player = None
        card.board = False
        card.save()
    models.Player.delete().where(models.Player.id == player_id).execute()
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
            card.discarded = patch_to_card.discarded
        if patch_to_card.player_id is not None:
            card.player_id = patch_to_card.player_id
        card.save()
        return card.serialize()
    else:
        raise HTTPException(
            status_code=403,
            detail="Player token incorrect"
        )

@router.post("/{first_player_id}/hand/switch/{second_player_id}")
def update_player_card(first_player_id: int, second_player_id: int):
    first_player = models.Player.get(first_player_id)
    second_player = models.Player.get(second_player_id)
    for first_player_card, second_player_card in itertools.zip_longest(list(first_player.cards.where(models.Card.board == False)), list(second_player.cards.where(models.Card.board == False))):
        if first_player_card is not None:
            first_player_card.player = second_player
            first_player_card.save()
        if second_player_card is not None:
            second_player_card.player = first_player
            second_player_card.save()
    return 200