from product_aggregator.database import db


class ProductModel(db.Model):

    __tablename__ = "Product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"Product(id = {self.id}, name = {self.name}, description = {self.description})"
