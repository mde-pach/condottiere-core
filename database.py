from peewee import *
import random

db = SqliteDatabase('condottiere.db')

def init_db():
    db.create_tables([Player, Deck, Card, Board])



class Player(Model):
    name = CharField(unique=True)
    secret = CharField(unique=True)
    class Meta:
        database = db

    def serialize(self):
        return {
            "name": self.name,
            "secret": self.secret,
            "id": self.id
        }

class Deck(Model):
    class Meta:
        database = db

class Board(Model):
    player = ForeignKeyField(Player, backref='board', unique=True)
    class Meta:
        database = db

    def serialize(self):
        return {
            "id": self.id,
            "player": self.player.id
        }

class Card(Model):
    name = CharField()
    player = ForeignKeyField(Player, backref='cards', null=True)
    deck = ForeignKeyField(Deck, backref='cards', null=True)
    board = ForeignKeyField(Board, backref='cards', null=True)
    order = FloatField()
    view_order = IntegerField()
    class Meta:
        database = db

    def serialize(self):
        return {
            "name": self.name,
            "id": self.id
        }
