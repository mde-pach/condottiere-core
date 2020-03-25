from peewee import *
import random

db = SqliteDatabase('condottiere.db')


class Game(Model):
    session_name = CharField(unique=True)
    name = CharField()
    need_money = BooleanField(default=False)
    can_give_cards = BooleanField(default=False)
    class Meta:
        database = db

class Deck(Model):
    name = CharField(null=True)
    game = ForeignKeyField(Game, backref='decks')
    class Meta:
        database = db

class Player(Model):
    name = CharField(unique=True)
    secret = CharField(unique=True)
    game = ForeignKeyField(Game, backref='players', null=True)
    money = IntegerField(default=0)
    class Meta:
        database = db

    def serialize(self):
        return {
            "name": self.name,
            "id": self.id,
            "money": self.money,
            'game_id': self.game_id
        }

class Card(Model):
    name = CharField()
    player = ForeignKeyField(Player, backref='cards', null=True)
    deck = ForeignKeyField(Deck, backref='cards', null=True)
    board = BooleanField(default=False)
    discarded = BooleanField(default=False)
    order = FloatField()
    view_order = IntegerField(null=True)
    coast = IntegerField(default=0)
    enable = BooleanField(default=True)
    class Meta:
        database = db

    def serialize(self):
        return {
            "name": self.name,
            "id": self.id,
            "enable": self.enable,
            "coast": self.coast
        }
