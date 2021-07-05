import os

import requests
from dotenv import load_dotenv

path_to_dotenv_file = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    ".env"
)
load_dotenv(path_to_dotenv_file)

ACCESS_TOKEN = os.environ.get('OFFERS_MS_ACCESS_TOKEN')

OFFERS_MS_BASE_URL = os.environ.get('OFFERS_MS_BASE_URL')
REGISTRATION_URL = OFFERS_MS_BASE_URL + "/products/register"
AUTHENTICATION_URL = OFFERS_MS_BASE_URL + "/auth"


def get_product_offers_url(product_id):
    return OFFERS_MS_BASE_URL + "/products/" + str(product_id) + "/offers"


def get_access_token():
    response = requests.post(AUTHENTICATION_URL)

    return response.json()['access_token']


def register_product(product):
    response = requests.post(
        REGISTRATION_URL,
        headers={'Bearer': ACCESS_TOKEN},
        data=product.to_json()
    )

    if response.status_code == 201:
        print(f"{product} was successfully registred")
    else:
        print(
            f"Registration of {product} failed with code {response.status_code}")


def get_offers_of_product(product):
    response = requests.get(
        get_product_offers_url(product.id),
        headers={'Bearer': ACCESS_TOKEN}
    )

    if response.status_code == 200:
        return response.json()
    else:
        print(
            f"Receiving of offers of {product} failed with code {response.status_code}")
