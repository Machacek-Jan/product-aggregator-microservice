from unittest import TestCase

import product_aggregator.main as main
from product_aggregator.database import db
from product_aggregator.model.product import Product

data_in_testing_database = [
    {"name": "name01", "description": "description01"},
    {"name": "name02", "description": "description02"},
    {"name": "name03", "description": "description03"}
]


def init_database(db):
    db.create_all()
    insert_data_into_database(db, data_in_testing_database)


def insert_data_into_database(db, data_to_be_inserted):
    for item in data_to_be_inserted:
        db.session.add(Product(item['name'], item['description']))
        db.session.commit()

class TestProductsAPIOperations(TestCase):

    def setUp(self):
        self.app = main.create_app("testing_database.db")
        self.app.config['TESTING'] = True

        init_database(db)

        self.client = self.app.test_client()

        self.endpoint = '/products'

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # ---------------------------------------------
    # Get products tests
    # ---------------------------------------------
    def test_get_products_valid_request_success(self):
        response = self.client.get(self.endpoint)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json), len(data_in_testing_database))

        for i, product in enumerate(data_in_testing_database):
            self.assertEqual(
                response.json[i]['name'], data_in_testing_database[i]['name'])
            self.assertEqual(
                response.json[i]['description'], data_in_testing_database[i]['description'])

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


class TestProductAPIOperations(TestCase):

    def setUp(self):
        self.app = main.create_app("testing_database.db")
        self.app.config['TESTING'] = True

        init_database(db)

        self.client = self.app.test_client()

        self.existing_id = 1
        self.nonexisting_id = 4
        self.endpoint_with_existing_id = "/products/" + str(self.existing_id)
        self.endpoint_with_nonexisting_id = "/products/" + str(self.nonexisting_id)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # ---------------------------------------------
    # Get product tests
    # ---------------------------------------------
    def test_get_product_valid_request_success(self):
        response = self.client.get(self.endpoint_with_existing_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], self.existing_id)

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
        self.assertEqual(response.json['id'], self.existing_id)
        self.assertEqual(response.json['name'], new_name)

    def test_patch_product_set_new_description_valid_request_success(self):
        new_description = 'test_new_desription'
        response = self.client.patch(
            self.endpoint_with_existing_id, 
            json={'description': new_description}
        )

        self.assertEqual(response.status_code, 205)
        self.assertEqual(response.json['id'], self.existing_id)
        self.assertEqual(response.json['description'], new_description)

    def test_patch_product_set_new_name_and_description_valid_request_success(self):
        new_name = 'test_new_name'
        new_description = 'test_new_desription'
        response = self.client.patch(
            self.endpoint_with_existing_id, 
            json={'name': new_name, 'description': new_description}
        )

        self.assertEqual(response.status_code, 205)
        self.assertEqual(response.json['id'], self.existing_id)
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
