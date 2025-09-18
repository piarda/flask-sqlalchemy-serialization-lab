from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from marshmallow import Schema, fields

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Relationship to review
    reviews = db.relationship('Review', back_populates='customer', cascade='all, delete-orphan')

    # Association proxy
    items = association_proxy('reviews', 'item')

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    # Relationship to review
    reviews = db.relationship('Review', back_populates='item', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'
    
class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)

    # Relationships
    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    def __repr__(self):
        return f'<Review {self.id}, Customer {self.customer_id}, Item {self.item_id}>'

class ReviewSchema(Schema):
    id = fields.Int()
    comment = fields.Str()
    # Nested customer without reviews to avoid recursion
    customer = fields.Nested('CustomerSchema', exclude=('reviews',))
    # Nested item without reviews to avoid recursion
    item = fields.Nested('ItemSchema', exclude=('reviews',))

class CustomerSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    reviews = fields.List(fields.Nested(ReviewSchema, exclude=('customer',)))

class ItemSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    price = fields.Float()
    reviews = fields.List(fields.Nested(ReviewSchema, exclude=('item',)))
