from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app import models
import random

router = APIRouter()



class Deck(BaseModel):
    name: str

@router.get("")
def get_deck():
    decks = models.Deck.get()
    return [
        {
            "id": deck.id,
            "cards": [card.serialize() for card in deck.cards]
        } for deck in models.Deck.select()
    ]

@router.get("/{deck_id}")
def get_deck(deck_id: int):
    deck = models.Deck.get(deck_id)
    return {
        "id": deck.id,
        "cards": [card.serialize() for card in deck.cards]
    }

@router.post("")
def create_deck(deck: Deck):
    if (models.Deck.select().count() == 0):
        new_deck = models.Deck()
        new_deck.save()
        create_deck_cards(new_deck)
        return [card.serialize() for card in new_deck.cards.order_by(models.Card.order)]
    raise HTTPException(
        status_code=400,
        detail="Deck already exists"
    )

@router.delete("/{deck_id}")
def delete_deck(deck_id: int):
    models.Deck.delete().execute()
    models.Card.delete().execute()

@router.post("/{deck_id}/shuffle")
def shuffle_game_deck(deck_id: int):
    deck = models.Deck.get(deck_id)
    for card in deck.cards:
        card.order = random.random()
        card.discarded = False
        card.save()
    return 200

@router.post("/{deck_id}/distribute/{player_id}")
def distribute_to_player(deck_id: int, player_id: int):
    # need authentication
    deck = models.Deck.get(deck_id)
    player = models.Player.get(player_id)

    card = deck.cards.where(models.Card.enable == True).where(models.Card.discarded == False).where(models.Card.player == None).order_by(models.Card.order).get()
    card.player = player
    card.board = False
    card.save()
    return 200