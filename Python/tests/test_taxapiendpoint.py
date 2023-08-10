"""
Ring2 Regression Test for Tax API
test_taxapiendpoint
Copyright 2022 Ring2 Communications LTD. All rights reserved.
"""

import sys
import json
import azure.cosmos.cosmos_client as cosmos_client
from azure.cosmos.partition_key import PartitionKey
from rts.rest import R2RestClient
import unittest
import config
import commonTestHelper
import os
from datetime import datetime
import redis
import random_address
from faker import Faker


class TestTaxApiEndpoint(unittest.TestCase):
    def setUp(self):
        self.rest = R2RestClient(config.TAXAPI_URL)
        self.headers = config.HEADERS
        self.fake = Faker()

        # Initialize the Cosmos client
        client = cosmos_client.CosmosClient(
            url=config._default_cosmos_db_url, credential=config._default_cosmos_db_pk
        )
        self.db = client.create_database_if_not_exists(
            id=config._default_cosmos_db_name)
        container = self.db.create_container_if_not_exists(
            id=config._default_cosmos_db_container,
            partition_key=PartitionKey(
                path='/id',
                kind='Hash'))

        self.itemList = list(container.read_all_items())

    def tearDown(self):
        print ('')
        
    def test_calculateTaxAllConfigInAzure(self):
        try:
            amount = commonTestHelper.round_up(config.RAND_NUMBER)
            for i in range(len(self.itemList)):
                items = []
                fixed_itemlist= self.itemList[i]
                taxAdvPayment = fixed_itemlist.get('taxAdvancePayments', None) 
                if (fixed_itemlist.get('location') is not None):
                    location = fixed_itemlist['location'].split("/")
                    country = location[0]
                    state = location[1] if len(location) > 1 else None
                else:
                    state = None
                
                area = fixed_itemlist['businessArea']
                if country == 'None':
                    print ('This config is either emptytax or no location')
                    break
                
                if 'chargeTypeMapping' not in fixed_itemlist and fixed_itemlist['handler'] == 'avalara':
                    for i in range(len(self.itemList)):
                        if (self.itemList[i]['id'] == 'CT::'+country):
                            fixed_itemlist['avalaraConfig']['chargeTypeMapping'] = self.itemList[i]['avalaraConfig']['chargeTypeMapping']
                            break
                
                # Percentage
                if (fixed_itemlist['handler'] == 'percentage'):
                    for i in range (len(fixed_itemlist['percentageConfig']['taxByChargeTypes'])):
                        items.append({
                            'ref': fixed_itemlist['percentageConfig']['taxByChargeTypes'][i]['chargeType'],
                            'chargeType': fixed_itemlist['percentageConfig']['taxByChargeTypes'][i]['chargeType'],
                            'prepaid': False,
                            'amount': amount
                        })
                    response = commonTestHelper.calculateTax(
                        area, country, items, datetime.utcnow().strftime("%Y-%m-%d"),
                        self.fake.address(), self.fake.city(), self.fake.state_abbr(), self.fake.postalcode())
                    rspContent = json.loads(response.content)
                    
                    tax_rate = fixed_itemlist['percentageConfig']['taxes'][0]['taxRate']
                    taxAmount = commonTestHelper.round_up(tax_rate * amount)

                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(rspContent['data']['invoiceString'], 'CT-123123')
                    self.assertEqual(
                            rspContent['data']['invoiceItemTaxes'][0]['taxes'][0]['taxRate'], tax_rate)
                    self.assertEqual(
                            rspContent['data']['invoiceItemTaxes'][0]['taxes'][0]['name'],
                            fixed_itemlist['percentageConfig']['taxes'][0]['name'])
                    self.assertEqual(
                            rspContent['data']['invoiceItemTaxes'][0]['taxes'][0]['taxAmount'],
                            taxAmount)
                    print (fixed_itemlist['id']+" calculation is passed")

                # Avalara
                elif (fixed_itemlist['handler'] == 'avalara'):            
                    avalara_items = []
                    exemp_avalara_taxid = []
                    exemp_avalara_items = []
                    exemptedTax = []
                    with open(os.getcwd()+'\\Python\\json\\address.json', 'r') as file:
                        address_data = json.load(file)
                    address = random_address.real_random_address_by_state(state)
                    for x in range (len(fixed_itemlist['avalaraConfig']['chargeTypeMapping'])):
                        items.append({
                            'ref': fixed_itemlist['avalaraConfig']['chargeTypeMapping'][x]['chargeType'],
                            'chargeType': fixed_itemlist['avalaraConfig']['chargeTypeMapping'][x]['chargeType'],
                            'prepaid': False,
                            'amount': amount
                        })
                        avalara_items.append({
                            "ref": fixed_itemlist['avalaraConfig']['chargeTypeMapping'][x]['chargeType'],
                            "chg": amount,
                            "sale": 1,
                            "incl": False,
                            "tran": fixed_itemlist['avalaraConfig']['chargeTypeMapping'][x]['trans'],
                            "serv": fixed_itemlist['avalaraConfig']['chargeTypeMapping'][x]['service'],
                            "dbt":False,
                            "adj": False
                        })
                    # Assign address
                    for i in range(len(address_data)):
                        if (address_data[i]["state"] == state or address_data[i]["country"] == country):
                            address = address_data[i]

                    # Get exempted tax                        
                    for i in range(len(fixed_itemlist["avalaraConfig"]["outputMapping"])):
                        if fixed_itemlist["avalaraConfig"]["outputMapping"][i]["exempted"] == 'true':
                            exemptedTax.append(fixed_itemlist["avalaraConfig"]["outputMapping"][i]["taxName"])
                            exemp_avalara_taxid.append(fixed_itemlist["avalaraConfig"]["outputMapping"][i]["avalaraTaxId"])
                    
                    # Add exemption to avalara items
                    if len(exemp_avalara_taxid) > 0:
                        for i in range(len(exemp_avalara_taxid)):
                            exemp_avalara_items.append(
                                {
                                    "tpe": exemp_avalara_taxid[i],
                                    "dom": 1,
                                    "loc": {
                                        "addr": address["address1"],
                                        "city": address["city"],
                                        "state": address["state"],
                                        "zip": address["postalCode"],
                                        "ctry": country 
                                        }
                                }
                            )
                    response = commonTestHelper.calculateTax(
                        area, country, items, datetime.utcnow().strftime("%Y-%m-%d"), address["address1"], address["city"],address["state"],address["postalCode"])
                    rspContent = json.loads(response.content)

                    avalaraResponse = commonTestHelper.calculateTaxWithAvalara(country,address["state"],address["city"],address["address1"],address["postalCode"], avalara_items, 
                                                                            exemp_avalara_items, datetime.utcnow().strftime("%Y-%m-%d"))
                    avalaraJson = json.loads(avalaraResponse.content)

                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(rspContent['data']['invoiceString'], 'CT-123123')
                    for i in range(len(rspContent['data']['invoiceItemTaxes'])):
                        self.assertEqual(avalaraJson['inv'][0]['itms'][i]['ref'], rspContent['data']['invoiceItemTaxes'][i]['ref'])
                        if (rspContent['data']['invoiceItemTaxes'][i]['ref'] == 'AdvancePayments'):
                            if (taxAdvPayment == str(True).lower()):
                                self.assertEqual(len(rspContent['data']['invoiceItemTaxes'][i]['taxes']), 1)
                            else:
                                self.assertEqual(len(rspContent['data']['invoiceItemTaxes'][i]['taxes']), 0)
                        else :    
                            for x in range(len(avalaraJson['inv'][0]['itms'][i]['txs'])):
                                if [element for element in exemptedTax if avalaraJson['inv'][0]['itms'][i]['txs'][x]['name'].lower() in element.lower()]:
                                    break
                                else:
                                    self.assertEqual(avalaraJson['inv'][0]['itms'][i]['txs'][x]['name'], rspContent['data']['invoiceItemTaxes'][i]['taxes'][x]['name'])
                                    self.assertEqual(avalaraJson['inv'][0]['itms'][i]['txs'][x]['tm'], rspContent['data']['invoiceItemTaxes'][i]['taxes'][x]['applicableAmount'])
                                    self.assertEqual(avalaraJson['inv'][0]['itms'][i]['txs'][x]['rate'], rspContent['data']['invoiceItemTaxes'][i]['taxes'][x]['taxRate'])
                                    self.assertEqual(commonTestHelper.round_up(avalaraJson['inv'][0]['itms'][i]['txs'][x]['tax']), rspContent['data']['invoiceItemTaxes'][i]['taxes'][x]['taxAmount'])
                    print (fixed_itemlist['id']+" calculation is passed")
            
            print ('test_passed')

        except AssertionError as e:
            print (str(e))
        except Exception as e:
            print (str(e))

if __name__ == '__main__':
    unittest.main()
