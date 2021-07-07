import requests

from product_aggregator.offers_ms_config import OFFERS_MS_BASE_URL, OFFERS_MS_ACCESS_TOKEN as ACCESS_TOKEN

REGISTRATION_URL = OFFERS_MS_BASE_URL + "/products/register"


def get_product_offers_url(product_id):
    return OFFERS_MS_BASE_URL + "/products/" + str(product_id) + "/offers"


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
