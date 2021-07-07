from unittest import TestCase

import product_aggregator.main as main
import product_aggregator.offers_ms_config as offers_ms_config
from product_aggregator.database import db
from product_aggregator.model.offer import Offer
from product_aggregator.model.product import Product

product_data_in_testing_database = [
    {"name": "name01", "description": "description01"},
    {"name": "name02", "description": "description02"},
    {"name": "name03", "description": "description03"}
]

offers_data_in_testing_database = [
    {'id': 1, 'product_id': 1, 'price': 10, 'items_in_stock': 10},
    {'id': 2, 'product_id': 1, 'price': 20, 'items_in_stock': 10},
    {'id': 3, 'product_id': 2, 'price': 30, 'items_in_stock': 10},
    {'id': 4, 'product_id': 3, 'price': 40, 'items_in_stock': 10}
]


def init_database(db):
    db.create_all()

    insert_products_data_into_database(db, product_data_in_testing_database)
    insert_offers_data_into_database(db, offers_data_in_testing_database)


def insert_products_data_into_database(db, data_to_be_inserted):
    for item in data_to_be_inserted:
        db.session.add(Product(item['name'], item['description']))
        db.session.commit()


def insert_offers_data_into_database(db, data_to_be_inserted):
    for item in data_to_be_inserted:
        db.session.add(
            Offer(item['product_id'], item['id'], item['price'], item['items_in_stock']))
        db.session.commit()


class TestAPIOperationsBaseClass(TestCase):
    def setUp(self):
        self.app = main.create_app("testing_database.db")
        self.app.config['TESTING'] = True

        # use invalid access token in communication with offers microservise during tests
        offers_ms_config.OFFERS_MS_ACCESS_TOKEN = "INVALID_ACCESS_TOKEN"

        init_database(db)

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestProductsAPIOperations(TestAPIOperationsBaseClass):

    endpoint = '/products'

    # ---------------------------------------------
    # Get products tests
    # ---------------------------------------------
    def test_get_products_valid_request_success(self):
        response = self.client.get(self.endpoint)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json), len(
            product_data_in_testing_database))

        for i in range(len(response.json)):
            self.assertEqual(
                response.json[i]['name'], product_data_in_testing_database[i]['name'])
            self.assertEqual(
                response.json[i]['description'], product_data_in_testing_database[i]['description'])

    # ---------------------------------------------
    # Post product tests
    # ---------------------------------------------
    def test_post_product_valid_request_success(self):
        new_product_data = {
            "name": "new_name",
            "description": "new_description"
        }

        response = self.client.post(self.endpoint, json=new_product_data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], new_product_data['name'])
        self.assertEqual(
            response.json['description'],
            new_product_data['description']
        )

    def test_post_product_without_name_fail(self):
        response = self.client.post(
            self.endpoint, json={'description': 'new_description'})

        self.assertEqual(response.status_code, 400)

    def test_post_product_without_description_fail(self):
        response = self.client.post(self.endpoint, json={'name': 'new_name'})

        self.assertEqual(response.status_code, 400)

    def test_post_product_empty_product_fail(self):
        response = self.client.post(self.endpoint, json={})

        self.assertEqual(response.status_code, 400)


class TestProductAPIOperations(TestAPIOperationsBaseClass):

    existing_product_id = 1
    nonexisting_product_id = 4
    endpoint_with_existing_id = f"/products/{existing_product_id}"
    endpoint_with_nonexisting_id = f"/products/{nonexisting_product_id}"

    # ---------------------------------------------
    # Get product tests
    # ---------------------------------------------
    def test_get_product_valid_request_success(self):
        response = self.client.get(self.endpoint_with_existing_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], self.existing_product_id)

    def test_get_product_with_nonexisting_id_fail(self):
        response = self.client.get(self.endpoint_with_nonexisting_id)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], "Product does not exist")

    # ---------------------------------------------
    # Patch product tests
    # ---------------------------------------------
    def test_patch_product_set_new_name_valid_request_success(self):
        new_name = 'test_new_name'
        response = self.client.patch(
            self.endpoint_with_existing_id,
            json={'name': new_name}
        )

        self.assertEqual(response.status_code, 205)
        self.assertEqual(response.json['id'], self.existing_product_id)
        self.assertEqual(response.json['name'], new_name)

    def test_patch_product_set_new_description_valid_request_success(self):
        new_description = 'test_new_desription'
        response = self.client.patch(
            self.endpoint_with_existing_id,
            json={'description': new_description}
        )

        self.assertEqual(response.status_code, 205)
        self.assertEqual(response.json['id'], self.existing_product_id)
        self.assertEqual(response.json['description'], new_description)

    def test_patch_product_set_new_name_and_description_valid_request_success(self):
        new_name = 'test_new_name'
        new_description = 'test_new_desription'
        response = self.client.patch(
            self.endpoint_with_existing_id,
            json={'name': new_name, 'description': new_description}
        )

        self.assertEqual(response.status_code, 205)
        self.assertEqual(response.json['id'], self.existing_product_id)
        self.assertEqual(response.json['name'], new_name)
        self.assertEqual(response.json['description'], new_description)

    def test_patch_product_nonexisting_id_fail(self):
        new_name = 'test_new_name'
        response = self.client.patch(
            self.endpoint_with_nonexisting_id,
            json={'name': new_name}
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], "Product does not exist")

    # ---------------------------------------------
    # Delete product tests
    # ---------------------------------------------
    def test_delete_product_valid_request_success(self):
        response = self.client.delete(self.endpoint_with_existing_id)

        self.assertEqual(response.status_code, 204)

    def test_delete_product_with_nonexisting_id_fail(self):
        response = self.client.delete(self.endpoint_with_nonexisting_id)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], "Product does not exist")


class TestProductOffersAPIOperations(TestAPIOperationsBaseClass):

    existing_product_id = 1
    nonexisting_product_id = 4
    endpoint_with_existing_id = f"/products/{existing_product_id}/offers"
    endpoint_with_nonexisting_id = f"/products/{nonexisting_product_id}/offers"

    # ---------------------------------------------
    # Get product offers tests
    # ---------------------------------------------
    def test_get_product_offers_valid_request_success(self):
        response = self.client.get(self.endpoint_with_existing_id)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json), 2)

        for offer_json in response.json:
            self.assertEqual(offer_json['product_id'],
                             self.existing_product_id)

    def test_get_product_offers_with_nonexisting_id_fail(self):
        response = self.client.get(self.endpoint_with_nonexisting_id)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json['message'], f"Product with id {self.nonexisting_product_id} does not exist")
