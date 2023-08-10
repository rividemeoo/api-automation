import config
from rts.rest import R2RestClient
import json
import math

_rest = R2RestClient(config.TAXAPI_URL)
_headers = config.HEADERS
_restAvalara = R2RestClient(config.AVALARA_API_URL)
_avalaraHeaders = config.AVALARA_HEADERS

def round_up(n, decimals=4):
    multiplier = 10 ** decimals 
    return math.ceil(n * multiplier) / multiplier

def calculateTax(businessArea, country, items, date, address, city, state, zip):
    route = '/v1/taxcalculations'
    body = {
            'businessArea': businessArea,
            'exceptionFlag': None,
            'invoice': {
                'invoiceString': 'CT-123123',
                'billToAddress': {
                'address': address,
                'city': city,
                'region': state,
                'zip': zip,
                'countryIso': country
                },
                'date': date,
                'items': items
            }
        }
    response = _rest.post(route, headers=_headers,
                         data=json.dumps(body))
    return response

def calculateTaxWithAvalara(country, state, city, address, zip, items, exemp_items, date):
    route = '/v2/afc/CalcTaxes'
    body = {
    "cmpn": {
        "bscl": 1,
        "svcl": 1,
        "fclt": False,
        "reg": True,
        "frch": False

    },
    "inv": [
        {
            "bill": {
                "ctry": country,
                "st": state,
                "cnty": None,
                "city": city,
                "addr": address,
                "zip": zip
            },
            "cust": 1,
            "lfln": False,
            "date": date,
            "itms": items,
            "exms": exemp_items,
            "invm": True,
            "dtl": True,
            "summ": True
                }
            ]
        }
    response = _restAvalara.post(route, headers=_avalaraHeaders,
                         data=json.dumps(body))
    return response

def getPcode(country, state, city, zip):
    route = '/v2/afc/PCode'
    body = {
        "CountryIso": country,
        "State": state,
        "County": None,
        "City": city,
        "ZipCode": zip,
        "BestMatch": True,
        "LimitResults": 1
            }
    response = _restAvalara.post(route, headers=_avalaraHeaders,
                         data=json.dumps(body))
    return response

def addressValidation(businessArea,exceptionFlag, address, city, state, zip, country):
    route = '/v1/addressValidations'
    body = {
            "businessArea": businessArea,
            "exceptionFlag": exceptionFlag,
            "address": {
                "address": address,
                "city": city,
                "region": state,
                "zip": zip,
                "countryIso": country
                        }
            }
    response = _rest.post(route, headers=_headers,
                         data=json.dumps(body))
    return response