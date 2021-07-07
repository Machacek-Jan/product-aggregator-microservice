from product_aggregator.database import db
from product_aggregator.model.offer import create_offers


def insert_offers_to_db(offers):
    db.session.add_all(offers)
    db.session.commit()


def update_offers_in_db(product, new_offers):
    for o in product.offers:
        db.session.delete(o)
    db.session.add_all(new_offers)

    db.session.commit()


def insert_offers_data_to_db(product, offers_data):
    if offers_data:
        offers = create_offers(product.id, offers_data)
        insert_offers_to_db(offers)


def update_offers_data_in_db(product, offers_data):
    if offers_data:
        offers = create_offers(product.id, offers_data)
        update_offers_in_db(product, offers)
