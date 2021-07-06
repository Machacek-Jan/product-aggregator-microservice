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

    def __init__(self, product_id, id, price, items_in_stock):
        self.product_id = product_id
        self.id = id
        self.price = price
        self.items_in_stock = items_in_stock

    def __repr__(self):
        return f"Offer(id = {self.id}, product_id = {self.product_id}, price = {self.price}, items_in_stock = {self.items_in_stock})"

    def to_json(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'price': self.price,
            'items_in_stock': self.items_in_stock
        }


def create_offer(product_id, offer_json_data):
    return Offer(product_id=product_id, id=offer_json_data['id'], price=offer_json_data['price'], items_in_stock=offer_json_data['items_in_stock'])


def create_offers(product_id, offers_json_data):
    return [create_offer(product_id, offer_json_data) for offer_json_data in offers_json_data]
