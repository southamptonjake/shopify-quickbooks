from flask import Flask
import shopify
from urllib2 import Request, urlopen, URLError
import httplib
import urllib
import requests
import json


##### Connects to the store
def SpecificOrder():

    API_KEY = "apikey"
    PASSWORD = "password"
    
    start_date = "2017-12-01"
    
    ADDRESS = "/orders.json"
    
    url = "https://%s:%s@myshop.myshopify.com/admin/orders.json" % (API_KEY, PASSWORD)
    
    r = requests.get(str(url),  headers={   "API_KEY" : API_KEY,
                                            "PASSWORD": PASSWORD })

    json_object = r.json()
    text_object = r.text

    #Get order information, dates and activities:
    order_id        = json_object["orders"][0]["id"]
    updated_at      = json_object["orders"][0]["updated_at"]
    created_at      = json_object["orders"][0]["created_at"]

    #Get list of orders:
    listoforders    = json_object["orders"][0]        

    #Get customer information
    # first_name      = json_object["orders"][0]["customer"]["first_name"]
    # last_name       = json_object["orders"][0]["customer"]["last_name"]
    # email           = json_object["orders"][0]["customer"]["email"]
    # address1        = json_object["orders"][0]["customer"]["default_address"]["address1"]
    # address2        = json_object["orders"][0]["customer"]["default_address"]["address2"]
    # city            = json_object["orders"][0]["customer"]["default_address"]["city"]
    # province        = json_object["orders"][0]["customer"]["default_address"]["province"]

    #Get order financial status
    status          = json_object["orders"][0]["financial_status"]

    for order in json_object["orders"]:
        print { "id"                : order["id"],
                "financial_status"  : order["financial_status"]}

    for order in 

        # newdict = { "id"        : order["id"],
        #             "status"    : order["financial_status"],
        #             "customer"  : 
        #                 {   name        : order["customer"]["first_name"],
        #                     last_name   : order["customer"]["last_name"],
        #                     email       : order["customer"]["email"],
        #                     address1    : order["customer"]["address1"],
        #                     address2    : order["customer"]["address2"]
        #                 }}