from flask_apscheduler import APScheduler

from product_aggregator.database import db
from product_aggregator.model.offer import create_offers
from product_aggregator.model.product import Product
from product_aggregator.offers_api_controller import get_offers_of_product

scheduler = APScheduler()


@scheduler.task('interval', id='update_product_offers', seconds=60)
def update_product_offers_job():
    with scheduler.app.app_context():

        products = db.session.query(Product).all()

        for product in products:
            offers_data = get_offers_of_product(product)
            
            new_offers = create_offers(product.id, offers_data)
            
            update_offers_in_db(product, new_offers)


def update_offers_in_db(product, new_offers):
    for o in product.offers:
        db.session.delete(o)
    db.session.add_all(new_offers)
    
    db.session.commit()
