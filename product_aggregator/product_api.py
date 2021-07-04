from flask_restful import Resource, reqparse, abort, fields, marshal_with

from product_aggregator.database import db
from product_aggregator.product_model import ProductModel


products_post_args = reqparse.RequestParser()
products_post_args.add_argument(
    "name", type=str, help="Name of the product is required", required=True
)
products_post_args.add_argument(
    "description", type=str, help="Description of the product is required", required=True
)


products_update_args = reqparse.RequestParser()
products_update_args.add_argument(
    "name", type=str, help="Name of the product"
)
products_update_args.add_argument(
    "description", type=str, help="Description of the product"
)


product_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String
}


class Product(Resource):
    @marshal_with(product_fields)
    def get(self, id):
        """
        Retrieves product with given id from database.

        :param id:  id of product to retrieve
        :return:    ProductModel with given id, 
                    404 if product with given id is not found
        """
        result = ProductModel.query.filter_by(id=id).first()
        if not result:
            abort(404, message=f"Product does not exist")
        return result

    @marshal_with(product_fields)
    def patch(self, id):
        """
        Updates product with given id in database.

        :param id:  id of product to update
        :return:    ProductModel with given id, 205 on successful update, 
                    404 if product with given id is not found
        """
        args = products_update_args.parse_args()
        result = ProductModel.query.filter_by(id=id).first()
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
        result = ProductModel.query.filter_by(id=id).first()
        if not result:
            abort(404, message="Product does not exist")

        db.session.delete(result)
        db.session.commit()

        return {}, 204


class Products(Resource):
    @marshal_with(product_fields)
    def get(self):
        """
        Retrieves all products from database.

        :return:    all ProductModels from database
        """
        results = ProductModel.query.all()

        return results, 200

    @marshal_with(product_fields)
    def post(self):
        """
        Creates product and adds it into database.

        :return:    created ProductModel, 201 on successful create
        """
        args = products_post_args.parse_args()
        product = ProductModel(
            name=args['name'], description=args['description'])

        db.session.add(product)
        db.session.commit()

        return product, 201
