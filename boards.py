from flask_restx import Namespace, Resource, fields
from database import Board, Card, Player

api = Namespace('boards', description='Boards related operations')

create_board = api.model('Create board', {
    'player_id': fields.Integer
})

card_on_board = api.model('Add Card to board', {
    'secret': fields.String,
    'card_id': fields.Integer
})

@api.route('')
class UntargetedBoard(Resource):
    def get(self):
        boards = {}
        for board in Board.select():
            boards[board.id] = board.serialize()
            boards[board.id]["cards"] = [card.serialize() for card in Card.select().where(Card.board == board).order_by(Card.view_order)]
        return boards
    
    @api.expect(create_board)
    def post(self):
        board = Board(player=Player.get(api.payload['player_id']))
        board.save()
        return 200

    def delete(self):
        Board.delete().execute()
        return 200

@api.route('/<int:board_id>/put')
class TargetedBoard(Resource):
    @api.expect(card_on_board)
    def post(self, board_id):
        board = Board.get(board_id)
        if board.player.secret == api.payload['secret']:
            card = Card.get(api.payload['card_id'])
            if card.deck != None:
                abort(403)
            card.board = board
            card.save()
        else:
            abort(403)
        return 200

@api.route('/<int:board_id>/get')
class TargetedBoard(Resource):
    @api.expect(card_on_board)
    def post(self, board_id):
        board = Board.get(board_id)
        if board.player.secret == api.payload['secret']:
            card = Card.get(api.payload['card_id'])
            if card.deck != None:
                abort(403)
            card.board = None
            card.save()
        else:
            abort(403)
        return 200
