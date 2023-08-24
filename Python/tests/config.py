#!/usr/bin/env python2
import os
import random
import sys
from datetime import datetime


RAND_NUMBER = random.uniform(0.1,9000.99999)

environment = os.environ["PYTHON_ENVIRONMENT"]

if environment == 'engr' or environment is None:
    _default_auth_token = 'LxfIUMbcrJWXiwvz0kymfOyTTuIMWPgISmKzTX8njUKYnLxyE/aHzQ=='
    _default_cosmos_db_url = 'https://usazw-ecdbcgn01.documents.azure.com:443/'
    _default_cosmos_db_pk = '8J9ieHGttLnwnW5VElews9SX6jHBpPhasVvMhTBewCIg7U73IXCDJyIjYLMKKMGDVvUzi2eidmDdfGPderZcpQ=='
    _default_cosmos_db_name = 'tax-settings'
    _default_cosmos_db_container = 'TaxConfig'
    _default_taxapi_url = 'https://usazw-efatapi01.azurewebsites.net/api'

elif environment == 'lab':
    _default_auth_token = 'fXDL6OxA2Befyct2ojCWVPuEAVz4mAEkX3XYHyhCtfZfAzFuNjK2yg=='
    _default_cosmos_db_url = 'https://usazw-lcdbtapi01.documents.azure.com:443/'
    _default_cosmos_db_pk = 'jwwahosw0L9t9palcvcqJ8LhS9o2QMKzBdb9QMSHYXWz8Fiizudj6RGyl81Rf3kNE9xZVOCffZiVZW8qtZxGnQ=='
    _default_cosmos_db_name = 'tax-settings'
    _default_cosmos_db_container = 'TaxConfig'
    _default_taxapi_url = 'https://usazw-lfatapi01.azurewebsites.net/api'

elif environment == 'prod':
    _default_auth_token = '89ZumQc7-Pa1lnT5b0vb_op79iQpo91_eXCOif35MK92AzFuIJAX6w=='
    _default_cosmos_db_url = 'https://usaznc-cdbtapi01.documents.azure.com:443/'
    _default_cosmos_db_pk = 'umoMsv7vXWzsBBE3OQoqYShQIl9RyNQP8nHvk4UvEvYmAH7wOWVl93jTzCBh7WELCmwmhXvwp5eHACDb3LKapw=='
    _default_cosmos_db_name = 'tax-settings'
    _default_cosmos_db_container = 'TaxConfig'
    _default_taxapi_url = 'https://usaznc-fatapi01.azurewebsites.net/api'


TAXAPI_URL = os.getenv('TAXAPI_TEST_URL', _default_taxapi_url)
AUTH_TOKEN = os.getenv('TAXAPI_TEST_APPTOKEN', _default_auth_token)
AVALARA_API_URL = 'https://communicationsua.avalara.net/api'
AVALARA_API_KEY = 'd2lsbHkud2lqYXlhQGVycmFpcGFzaWZpay5jb206TG9vcGVyczEyMyE='

HEADERS = {
    "x-functions-key": AUTH_TOKEN,
    "Content-Type": "application/json"
}

AVALARA_HEADERS = {
    "api_key": AVALARA_API_KEY,
    "Content-Type": "application/json"
}
