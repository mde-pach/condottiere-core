import random
import string
from flask import abort, request
from flask_restx import Namespace, Resource, fields
from database import Player, Card, Deck

api = Namespace('players', description='Players related operations')

player = api.model('Player', {
    'name': fields.String
})
auth = api.model('Auth', {
    'secret': fields.String
})

throw_card = api.model('Throw Card to deck', {
    'secret': fields.String,
    'card_id': fields.Integer
})

@api.route('')
class UntargetedPlayer(Resource):
    def get(self):
        return {player['id']: {'name': player['name'], 'id': player['id']} for player in Player.select().dicts()}

    @api.expect(player)
    def post(self):
        player = Player(name=api.payload['name'], secret=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25)))
        player.save()
        return player.serialize()

    def delete(self):
        for card in Card.select().where(Card.player != None):
            card.player = None
            card.board = None
            card.save()
        Player.delete().execute()

@api.route('/<int:player_id>')
class TargetedPlayer(Resource):
    def get(self, player_id):
        try:
            Player.get(player_id)
            return 200
        except:
            abort(404)

@api.route('/<int:player_id>/auth')
class PlayerAuth(Resource):
    @api.expect(auth)
    def post(self, player_id):
        if Player.get(player_id).secret == api.payload['secret']:
            return 200
        else:
            abort(403)

@api.route('/<int:player_id>/cards')
class TargetedPlayerCards(Resource):
    def get(self, player_id):
        player = None
        try:
            player = Player.get(player_id)
        except:
            abort(404)
        if player.secret == request.headers['x-secret-token']:
            return [card.serialize() for card in Card.select().where(Card.player == player).where(Card.board == None).order_by(Card.view_order)]
        else:
            abort(403)

@api.route('/<int:player_id>/cards/throw')
class TargetedPlayerCardsThrow(Resource):
    def post(self, player_id):
        player = Player.get(player_id)
        if player.secret == api.payload['secret']:
            card = Card.get(api.payload['card_id'])
            card.board = None
            card.deck = Deck.get()
            card.player = None
            card.save()
            return 200
        else:
            abort(403)



# @api.route('/<string:player_name>/pick/<int:number>')
# class TargetedPlayerPick(Resource):
#     def get(self, player_name, number):
#         global DECK
#         random.shuffle(DECK)
#         cards = DECK[:number]
#         PLAYERS[player_name]['hand'] += cards
#         return PLAYERS[player_name]

# @api.route('/<string:player_name>/put/<string:card_name>')
# class TargetedPlayerPut(Resource):
#     def get(self, player_name, card_name):
#         if (card_name in PLAYERS[player_name]['hand']):
#             PLAYERS[player_name]['hand'].remove(card_name)
#             PLAYERS[player_name]['board'] += card_name
#         return PLAYERS[player_name]

# @api.route('/<string:player_name>/get/<string:card_name>')
# class TargetedPlayerGet(Resource):
#     def get(self, player_name, card_name):
#         if (card_name in PLAYERS[player_name]['board']):
#             PLAYERS[player_name]['board'].remove(card_name)
#             PLAYERS[player_name]['hand'] += card_name
#         return PLAYERS[player_name]
