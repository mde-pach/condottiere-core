from peewee import *
import random

db = SqliteDatabase('condottiere.db')


class Deck(Model):
    class Meta:
        database = db

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

class Card(Model):
    name = CharField()
    player = ForeignKeyField(Player, backref='cards', null=True)
    deck = ForeignKeyField(Deck, backref='cards', null=True)
    board = BooleanField(default=False)
    order = FloatField()
    view_order = IntegerField()
    class Meta:
        database = db

    def serialize(self):
        return {
            "name": self.name,
            "id": self.id
        }
