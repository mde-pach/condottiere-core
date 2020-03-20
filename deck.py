import random
from flask_restx import Namespace, Resource, fields
from database import Deck, Card, Player
from flask import abort

api = Namespace('deck', description='Deck related operations')

deck_composition = {
    "Hiver": {
        "number": 3,
        "view_order": 11
    },
    "Printemps": {
        "number": 3,
        "view_order": 10
    },
    "Eveque": {
        "number": 6,
        "view_order": 13
    },
    "Courtisane": {
        "number": 12,
        "view_order": 0
    },
    "Tambour": {
        "number": 6,
        "view_order": 12
    },
    "Heroine": {
        "number": 3,
        "view_order": 8
    },
    "Epouvantail": {
        "number": 16,
        "view_order": 9
    },
    "Reddition": {
        "number": 3,
        "view_order": 14
    },
    "Mercenaire 1": {
        "number": 10,
        "view_order": 1
    },
    "Mercenaire 2": {
        "number": 8,
        "view_order": 2
    },
    "Mercenaire 3": {
        "number": 8,
        "view_order": 3
    },
    "Mercenaire 4": {
        "number": 8,
        "view_order": 4
    },
    "Mercenaire 5": {
        "number": 8,
        "view_order": 5
    },
    "Mercenaire 6": {
        "number": 8,
        "view_order": 6
    },
    "Mercenaire 10": {
        "number": 8,
        "view_order": 7
    }
}

auth = api.model('Auth', {
    'secret': fields.String
})

card_pick = api.model('Card picking from deck', {
    'card_number': fields.Integer
})


def create_deck(deck):
    for card_name, rules in deck_composition.items():
        for i in range(0, int(rules['number'])):
            card = Card(name=card_name, deck=deck, order=random.random(), view_order=rules["view_order"])
            card.save()

@api.route('')
class UntargetedDeck(Resource):
    def get(self):
        deck = Deck.get()
        return [card.serialize() for card in Card.select().where(Card.deck == deck).order_by(Card.order)]

    def post(self):
        if (Deck.select().count() == 0):
            deck = Deck()
            deck.save()
            create_deck(deck)
            return [card.serialize() for card in Card.select().where(Card.deck == deck).order_by(Card.order)]
        abort(400)

    def delete(self):
        Card.delete().execute()
        Deck.delete().execute()
        return 200

@api.route('/shuffle')
class DeckShuffle(Resource):
    def get(self):
        deck = Deck.get()
        for card in Card.select().where(Card.deck == deck):
            card.order = random.random()
            card.save()
        return 200

@api.route('/pick/<int:player_id>')
class DeckPick(Resource):
    @api.expect(card_pick)
    def post(self, player_id):
        player = Player.get(player_id)
        deck = Deck.get()
        for i in range(0, api.payload['card_number']):
            card = Card.select().where(Card.deck == deck).order_by(Card.order).limit(1)[0]
            card.player = player
            card.deck = None
            card.save()
        return 200

