import os

import requests
from dotenv import load_dotenv

path_to_dotenv_file = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    ".env"
)
load_dotenv(path_to_dotenv_file)

OFFERS_MS_BASE_URL = os.environ.get('OFFERS_MS_BASE_URL')
OFFERS_MS_AUTHENTICATION_URL = OFFERS_MS_BASE_URL + "/auth"

# get new access token if it is not defined
if os.environ.get('OFFERS_MS_ACCESS_TOKEN') is None:

    # get new access token
    access_token = requests.post(OFFERS_MS_AUTHENTICATION_URL).json()['access_token']

    # save access token to .env file
    with open(path_to_dotenv_file, 'a') as f:
        f.write(f"OFFERS_MS_ACCESS_TOKEN={access_token}\n")

load_dotenv(path_to_dotenv_file)
OFFERS_MS_ACCESS_TOKEN = os.environ.get('OFFERS_MS_ACCESS_TOKEN')
