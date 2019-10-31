import sqlite3
from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'
    sqstore = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    category = db.Column(db.String(80))

    # with lazy is now a querybuilder
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name, category):
        self.name = name
        self.category = category

    def json(self):
        return {'name':self.name,
        'category': self.category,
        'items': [item.json() for item in self.items.all()]}
        # .all because self.items is a querybuilder

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self): #insert and update
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
