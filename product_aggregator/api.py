from flask_restful import Resource, abort, fields, marshal_with, reqparse

from product_aggregator.database import db
from product_aggregator.model.product import Product
from product_aggregator.offers_dao import insert_offers_data_to_db
from product_aggregator.offers_ms_controller import register_product, retrieve_offers_of_product

product_post_args = reqparse.RequestParser()
product_post_args.add_argument(
    "name", type=str, help="Name of the product is required", required=True
)
product_post_args.add_argument(
    "description", type=str, help="Description of the product is required", required=True
)

product_update_args = reqparse.RequestParser()
product_update_args.add_argument(
    "name", type=str, help="Name of the product"
)
product_update_args.add_argument(
    "description", type=str, help="Description of the product"
)


product_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String
}

offer_fields = {
    'id': fields.Integer,
    'product_id': fields.Integer,
    'price': fields.Integer,
    'items_in_stock': fields.Integer
}


class ProductResource(Resource):
    @marshal_with(product_fields)
    def get(self, id):
        """
        Retrieves product with given id from database.

        :param id:  id of product to retrieve
        :return:    Product with given id, 
                    404 if product with given id is not found
        """
        result = Product.query.filter_by(id=id).first()
        if not result:
            abort(404, message=f"Product does not exist")
        return result

    @marshal_with(product_fields)
    def patch(self, id):
        """
        Updates product with given id in database.

        :param id:  id of product to update
        :return:    Product with given id, 205 on successful update, 
                    404 if product with given id is not found
        """
        args = product_update_args.parse_args()
        result = Product.query.filter_by(id=id).first()
        if not result:
            abort(404, message=f"Product does not exist")

        if args['name']:
            result.name = args['name']
        if args['description']:
            result.description = args['description']

        db.session.merge(result)
        db.session.commit()

        return result, 205

    def delete(self, id):
        """
        Delete product with given id from database.

        :param id:  id of product to delete
        :return:    204 on successful delete, 
                    404 if product with given id is not found
        """
        result = Product.query.filter_by(id=id).first()
        if not result:
            abort(404, message="Product does not exist")

        db.session.delete(result)
        db.session.commit()

        return {}, 204


class ProductsResource(Resource):
    @marshal_with(product_fields)
    def get(self):
        """
        Retrieves all products from database.

        :return:    all Products from database
        """
        results = Product.query.all()

        return results, 200

    @marshal_with(product_fields)
    def post(self):
        """
        Creates product and adds it into database. Register created product to offers 
        microservise. Retrieves offers of this product and saves them to database. 

        :return:    created Product, 201 on successful create
        """
        args = product_post_args.parse_args()
        product = Product(
            name=args['name'],
            description=args['description']
        )

        db.session.add(product)
        db.session.commit()

        register_product(product)

        offers_data = retrieve_offers_of_product(product)

        insert_offers_data_to_db(product, offers_data)

        return product, 201


class ProductOffersResource(Resource):
    @marshal_with(offer_fields)
    def get(self, product_id):
        """
        Retrieves all offers of the product with given product_id from database.

        :param product_id:  id of product whose all offers are returned
        :return:            all offers of the product with given product_id from database
                            200 on successful read, 
                            404 if product with given product_id is not found
        """
        product = Product.query.filter_by(id=product_id).first()
        if not product:
            abort(404, message=f"Product with id {product_id} does not exist")

        return product.offers, 200
