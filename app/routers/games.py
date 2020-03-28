from fastapi import APIRouter, Header
from pydantic import BaseModel
from app import models
import random

router = APIRouter()

GAMES = {
    "condottiere": {
        "can_give_cards": False,
        "need_money": False,
        "hand_count": False,
        "decks": [
            {
                "name": "deck principal",
                "cards": {
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
            }
        ],
    },
    "citadelle": {
        "can_give_cards": True,
        "need_money": True,
        "hand_count": True,
        "decks": [
            {
                "name": "Deck de quartier",
                "cards": {
                    "Cour des miracles": {
                        "number": 1,

                    },
                    "Poudriere": {
                        "number": 1,

                    },
                    "Carriere": {
                        "number": 1,

                    },
                    "Chantier": {
                        "number": 1,

                    },
                    "Bibliotheque": {
                        "number": 1,

                    },
                    "Ecuries": {
                        "number": 1,

                    },
                    "Theatre": {
                        "number": 1,

                    },
                    "Hospice": {
                        "number": 1,

                    },
                    "Parc": {
                        "number": 1,

                    },
                    "Necropole": {
                        "number": 1,

                    },
                    "Capitole": {
                        "number": 1,

                    },
                    "Forge": {
                        "number": 1,

                    },
                    "Manufacture": {
                        "number": 1,

                    },
                    "Donjon": {
                        "number": 1,

                    },
                    "Catacombes": {
                        "number": 1,

                    },
                    "Grande muraille": {
                        "number": 1,

                    },
                    "Observatoire": {
                        "number": 1,

                    },
                    "Fontaine aux souhaits": {
                        "number": 1,

                    },
                    "Statue equestre": {
                        "number": 1,

                    },
                    "Tresor imperial": {
                        "number": 1,

                    },
                    "Basilique": {
                        "number": 1,

                    },
                    "Dracoport": {
                        "number": 1,

                    },
                    "Ecole de magie": {
                        "number": 1,

                    },
                    "Laboratoire": {
                        "number": 1,

                    },
                    "Mine d'or": {
                        "number": 1,

                    },
                    "Monument": {
                        "number": 1,

                    },
                    "Tripot": {
                        "number": 1,

                    },
                    "Tour d'ivoire": {
                        "number": 1,

                    },
                    "Musee": {
                        "number": 1,

                    },
                    "Salle des cartes": {
                        "number": 1,

                    },
                    "Chateau": {
                        "number": 4,

                    },
                    "Manoir": {
                        "number": 5,

                    },
                    "Cathedrale": {
                        "number": 2,

                    },
                    "Eglise": {
                        "number": 3,

                    },
                    "Hotel de ville": {
                        "number": 2,

                    },
                    "Forteresse": {
                        "number": 1,

                    },
                    "Comptoir": {
                        "number": 3,

                    },
                    "Temple": {
                        "number": 3,

                    },
                    "Palais": {
                        "number": 3,

                    },
                    "Port": {
                        "number": 3,

                    },
                    "Caserne": {
                        "number": 3,

                    },
                    "Monastere": {
                        "number": 3,

                    },
                    "Taverne": {
                        "number": 5,

                    },
                    "Prison": {
                        "number": 3,

                    },
                    "Marche": {
                        "number": 4,

                    },
                    "Tour de guet": {
                        "number": 3,

                    },
                    "Echoppe": {
                        "number": 3,

                    }
                }
            },
            {
                "name": "Deck de personnages",
                "cards": {
                    "Echevin": {
                        "number": 1,
                        "view_order": 1,
                        "enable": False
                    },
                    "Sorciere": {
                        "number": 1,
                        "view_order": 1,
                        "enable": False
                    },
                    "Assassin": {
                        "number": 1,
                        "view_order": 1
                    },
                    "Espion": {
                        "number": 1,
                        "view_order": 2,
                        "enable": False
                    },
                    "Voleur": {
                        "number": 1,
                        "view_order": 2
                    },
                    "Maitre-chanteuse": {
                        "number": 1,
                        "view_order": 2,
                        "enable": False
                    },
                    "Voyante": {
                        "number": 1,
                        "view_order": 3,
                        "enable": False
                    },
                    "Magicienne": {
                        "number": 1,
                        "view_order": 3
                    },
                    "Sorcier": {
                        "number": 1,
                        "view_order": 3,
                        "enable": False
                    },
                    "Roi": {
                        "number": 1,
                        "view_order": 4
                    },
                    "Patricien": {
                        "number": 1,
                        "view_order": 4,
                        "enable": False
                    },
                    "Empereur": {
                        "number": 1,
                        "view_order": 4,
                        "enable": False
                    },
                    "Abbe": {
                        "number": 1,
                        "view_order": 5,
                        "enable": False
                    },
                    "Cardinal": {
                        "number": 1,
                        "view_order": 5,
                        "enable": False
                    },
                    "Eveque": {
                        "number": 1,
                        "view_order": 5
                    },
                    "Negociant": {
                        "number": 1,
                        "view_order": 6,
                        "enable": False
                    },
                    "Alchimiste": {
                        "number": 1,
                        "view_order": 6,
                        "enable": False
                    },
                    "Marchande": {
                        "number": 1,
                        "view_order": 6
                    },
                    "Architecte": {
                        "number": 1,
                        "view_order": 7
                    },
                    "Navigatrice": {
                        "number": 1,
                        "view_order": 7,
                        "enable": False
                    },
                    "Archiviste": {
                        "number": 1,
                        "view_order": 7,
                        "enable": False
                    },
                    "Condottiere": {
                        "number": 1,
                        "view_order": 8
                    },
                    "Capitaine": {
                        "number": 1,
                        "view_order": 8,
                        "enable": False
                    },
                    "Diplomate": {
                        "number": 1,
                        "view_order": 8,
                        "enable": False
                    },
                    "Bailli": {
                        "number": 1,
                        "view_order": 9,
                        "enable": False
                    },
                    "Artiste": {
                        "number": 1,
                        "view_order": 9,
                        "enable": False
                    },
                    "Reine": {
                        "number": 1,
                        "view_order": 9,
                        "enable": False
                    }
                }
            }
        ]
    }
}

class Game(BaseModel):
    name: str
    session_name: str

def create_deck(game):
    for deck in GAMES[game.name]["decks"]:
        new_deck = models.Deck(game=game, name=deck["name"])
        new_deck.save()
        for card_name, rules in deck["cards"].items():
            for i in range(0, int(rules['number'])):
                card = models.Card(name=card_name, deck=new_deck, order=random.random(), view_order=rules.get("view_order"), enable=rules.get("enable", True))
                card.save()

@router.get("")
def get_games():
    return [
        {
            "id": game.id,
            "name": game.name,
            "session_name": game.session_name,
            "need_money": game.need_money,
            "can_give_cards": game.can_give_cards,
            "hand_count": game.hand_count,
            "players": [
                {
                    'name': player.name,
                    'id': player.id,
                    'hand_count': player.cards.where(models.Card.deck << game.decks).where(models.Card.board == False).count() if game.hand_count is True else (False if player.cards.where(models.Card.deck << game.decks).where(models.Card.board == False).count() == 0 else True),
                    'money': player.money if game.need_money is True else None,
                    'board': [card.serialize() for card in player.cards.where(models.Card.board == True).where(models.Card.deck << game.decks).order_by(models.Card.view_order)],
                    'game_id': player.game_id
                } for player in models.Player.select().where(models.Player.game == game)
            ],
            "decks": [
                {
                    "id": deck.id,
                    "name": deck.name,
                    "count": len(deck.cards.where(models.Card.enable == True).where(models.Card.discarded == False).where(models.Card.player == None))
                } for deck in game.decks
            ]
        } for game in models.Game.select()
    ]

@router.get("/{game_id}")
def get_game(game_id: int):
    game = models.Game.get(game_id)
    return {
        "id": game.id,
        "name": game.name,
        "session_name": game.session_name,
        "need_money": game.need_money,
        "can_give_cards": game.can_give_cards,
        "hand_count": game.hand_count,
        "players": [
            {
                'name': player.name,
                'id': player.id,
                'hand_count': player.cards.where(models.Card.deck << game.decks).where(models.Card.board == False).count() if game.hand_count is True else (False if player.cards.where(models.Card.deck << game.decks).where(models.Card.board == False).count() == 0 else True),
                'money': player.money if game.need_money is True else None,
                'board': [card.serialize() for card in player.cards.where(models.Card.board == True).where(models.Card.deck << game.decks).order_by(models.Card.view_order)],
                'game_id': player.game_id
            } for player in models.Player.select().where(models.Player.game == game)
        ],
        "decks": [
            {
                "id": deck.id,
                "name": deck.name,
                "count": len(deck.cards.where(models.Card.enable == True).where(models.Card.discarded == False).where(models.Card.player == None))
            } for deck in game.decks
        ]
    }


@router.post("")
def create_game(game: Game):
    new_game = models.Game(
        name=game.name,
        session_name=game.session_name,
        need_money=GAMES[game.name].get("need_money", False),
        can_give_cards=GAMES[game.name].get("can_give_cards", False),
        hand_count=GAMES[game.name].get("hand_count", False)
    )
    new_game.save()
    create_deck(new_game)
    return {
        "id": new_game.id,
        "name": new_game.name,
        "session_name": new_game.session_name,
        "players": [
            player.serialize() for player in models.Player.select().where(models.Player.game == new_game)
        ]
    }

@router.delete("/{game_id}")
def delete_game(game_id: int):
    game = models.Game.get(game_id)
    for deck in models.Deck.select().where(models.Deck.game == game):
        models.Card.delete().where(models.Card.deck == deck).execute()
        deck.delete_instance()
    for player in models.Player.select().where(game == game):
        player.game = None
        player.save()
    game.delete_instance()
    return 200

@router.get("/{game_id}/decks")
def get_decks(game_id: int):
    deck = models.Deck.get()
    return [card.serialize() for card in deck.cards]

