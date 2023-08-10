"""
Ring2 Regression Test for Tax API
test_healthCheck
Copyright 2018 Ring2 Communications LTD. All rights reserved.
"""

import unittest
import requests
import config
import pyodbc
from rts.rest import R2RestClient
import json
import traceback
import sys


class TestHealthCheckEndpoint(unittest.TestCase):

    def setUp(self):
        self.rest = R2RestClient(config.TAXAPI_URL)
        self.headers = config.HEADERS

    def test_HealthCheck200Response(self):
        try:
            route = '/v1/healthcheck'
            response = self.rest.get(route, headers=self.headers)
            print (response.content)
            rspContent = json.loads(response.content)
            print ('status_code:' + str(response.status_code))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(rspContent["status"], 'Healthy')

            print('test_passed')
        except AssertionError as e:
            print ('An error occurred: {}'.format(e))


if __name__ == "__main__":
    unittest.main()
