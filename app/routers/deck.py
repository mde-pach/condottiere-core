from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app import models
import random

router = APIRouter()

deck_composition = {
    "Hiver": {
        "number": 3,
        "view_order": 2
    },
    "Printemps": {
        "number": 3,
        "view_order": 1
    },
    "Eveque": {
        "number": 6,
        "view_order": 13
    },
    "Courtisane": {
        "number": 12,
        "view_order": 10
    },
    "Tambour": {
        "number": 6,
        "view_order": 0
    },
    "Heroine": {
        "number": 3,
        "view_order": 11
    },
    "Epouvantail": {
        "number": 16,
        "view_order": 12
    },
    "Reddition": {
        "number": 3,
        "view_order": 14
    },
    "Mercenaire 1": {
        "number": 10,
        "view_order": 3
    },
    "Mercenaire 2": {
        "number": 8,
        "view_order": 4
    },
    "Mercenaire 3": {
        "number": 8,
        "view_order": 5
    },
    "Mercenaire 4": {
        "number": 8,
        "view_order": 6
    },
    "Mercenaire 5": {
        "number": 8,
        "view_order": 7
    },
    "Mercenaire 6": {
        "number": 8,
        "view_order": 8
    },
    "Mercenaire 10": {
        "number": 8,
        "view_order": 9
    }
}

class Deck(BaseModel):
    pass

def create_deck_cards(deck):
    for card_name, rules in deck_composition.items():
        for i in range(0, int(rules['number'])):
            card = models.Card(name=card_name, deck=deck, order=random.random(), view_order=rules["view_order"])
            card.save()

@router.post("")
def create_deck():
    if (models.Deck.select().count() == 0):
        deck = models.Deck()
        deck.save()
        create_deck_cards(deck)
        return [card.serialize() for card in deck.cards.order_by(models.Card.order)]
    raise HTTPException(
        status_code=400,
        detail="Deck already exists"
    )

@router.get("")
def get_deck():
    deck = models.Deck.get()
    return [card.serialize() for card in deck.cards.order_by(models.Card.order)]

@router.delete("")
def delete_deck():
    models.Deck.delete().execute()
    models.Card.delete().execute()

@router.post("/shuffle")
def shuffle_deck():
    deck = models.Deck.get()
    for card in deck.cards:
        card.order = random.random()
        card.save()
    return 200

@router.post("/distribute/{player_id}")
def distribute_to_player(player_id: int):
    # need authentication
    player = models.Player.get(player_id)
    deck = models.Deck.get()
    card = deck.cards.where(models.Card.player == None).order_by(models.Card.order).get()
    card.player = player
    card.board = False
    card.save()
    return None
