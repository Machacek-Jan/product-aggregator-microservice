import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from flask_restful import Api

from product_aggregator.database import db
from product_aggregator.product_api import Product, Products


def create_app(db_name):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # dynamically bind SQLAlchemy to application
    db.init_app(app)
    app.app_context().push()

    basedir = os.path.abspath(os.path.dirname(__file__))

    # create database if it does not exist
    if not os.path.exists(os.path.join(basedir, db_name)):
        db.create_all()

    # set up products API
    api = Api(app)
    api.add_resource(Products, '/products')
    api.add_resource(Product, '/products/<int:id>')

    return app


if __name__ == '__main__':
    app = create_app("database.db")
    app.run(debug=True)  # TODO remove debug mode after development
