import random
import string
from flask import Flask, request, abort
from flask_restx import Api, Resource, fields
from flask_cors import CORS, cross_origin
from players import api as players_api
from deck import api as deck_api
from boards import api as boards_api
from database import init_db

init_db()
authorizations = {
    'secret': {
        'type': 'secret',
        'in': 'header',
        'name': 'X-SECRET'
    }
}

app = Flask(__name__)
CORS(app)
api = Api(app, authorizations=authorizations)

api.add_namespace(players_api)
api.add_namespace(deck_api)
api.add_namespace(boards_api)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,x-secret-token')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
    app.run(debug=True)
