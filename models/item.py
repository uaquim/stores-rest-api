import sqlite3
from db import db
from models.store import StoreModel

class ItemModel(db.Model):
    __tablename__ = 'items'
    sqitem = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    sqstore = db.Column(db.Integer, db.ForeignKey('stores.sqstore'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, sqstore):
        self.name = name
        self.price = price
        self.sqstore = sqstore

    def json(self):
        return {'name':self.name, 'price':self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self): #insert and update
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
