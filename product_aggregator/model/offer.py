from product_aggregator.database import db


class Offer(db.Model):
    """
    Flask-SQLAlchemy database model representing an offer of the product.
    """

    __tablename__ = "Offer"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("Product.id"), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    items_in_stock = db.Column(db.Integer, nullable=False)

    def __init__(self, product_id, price, items_in_stock):
        self.product_id = product_id
        self.price = price
        self.items_in_stock = items_in_stock

    def __repr__(self):
        return f"Offer(id = {self.id}, product_id = {self.product_id}, price = {self.price}, items_in_stock = {self.items_in_stock})"
