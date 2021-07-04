from product_aggregator.database import db
from product_aggregator.model.offer import Offer


class Product(db.Model):
    """
    Flask-SQLAlchemy database model representing a product.
    """

    __tablename__ = "Product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    offers = db.relationship('Offer', backref='offer')

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"Product(id = {self.id}, name = {self.name}, description = {self.description})"
