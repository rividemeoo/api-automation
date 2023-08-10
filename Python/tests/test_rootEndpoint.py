"""
Ring2 Regression Test for CT API
test_rootEndpoint
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


class TestRootEndpoint(unittest.TestCase):

    def setUp(self):
        self.rest = R2RestClient(config.TAXAPI_URL)
        self.headers = config.HEADERS

    def test_rootEndpoint200Response(self):
        try:
            route = '/v1/version'
            response = self.rest.get(route, headers=self.headers)
            print (response.content)
            print ('status_code:' + str(response.status_code))

            self.assertEqual(response.status_code, 200)
            print('test_passed')
        except AssertionError as e:
            print ('An error occurred: {}'.format(e))


if __name__ == "__main__":
    unittest.main()
