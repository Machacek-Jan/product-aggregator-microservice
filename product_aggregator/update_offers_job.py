from flask_apscheduler import APScheduler

from product_aggregator.database import db
from product_aggregator.model.product import Product
from product_aggregator.offers_dao import update_offers_data_in_db
from product_aggregator.offers_ms_controller import retrieve_offers_of_product

scheduler = APScheduler()


@scheduler.task('interval', id='update_product_offers', seconds=60)
def update_product_offers_job():
    with scheduler.app.app_context():

        products = db.session.query(Product).all()
        
        for product in products:
            offers_data = retrieve_offers_of_product(product)
            
            update_offers_data_in_db(product, offers_data)
