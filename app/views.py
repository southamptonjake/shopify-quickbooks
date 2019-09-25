from app import app
from flask import Flask, render_template, request, redirect, url_for
import json, jsonify, collections, itertools, csv
import requests
import config as cfg
from . import models
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes


access_token = ""
refresh_token = ""

@app.route("/redirectEnvironment")
def redirect():
    print("hi")
    return "hi"


@app.route("/")
def index():
    return request.args.get('text', '')

################################################################################### SHOPIFY ORDER WEBHOOK

@app.route("/shopifyorder",methods = ['POST','GET'])
def get_new_order():

    # this will have the order
    #payload = request.json
    payload = json.load(open('app/objects/shop_order_webhook.json'))

    so = models.ShopOrder(payload['id'],payload['total_price'],payload['subtotal_price'],payload['financial_status'],payload['total_discounts'],
    payload['user_id'],payload['location_id'],payload['line_items'])

    sc = models.ShopCustomer(payload['customer']['id'],payload['customer']['email'],payload['customer']['first_name'],payload['customer']['last_name'],
    payload['customer']['default_address']['address1'],payload['customer']['default_address']['address2'],payload['customer']['default_address']['city'],
    payload['customer']['default_address']['province'],payload['customer']['default_address']['phone'])

    ois = []

    for item in payload['line_items']:
        oi = models.ShopOrderItems(item['id'],item['title'],item['quantity'],item['price'],item['sku'],item['product_id'], item['total_discount'])
        ois.append(oi)

    print(sc.email)

    requests.post(qbo_access_toke())
    #quickbooks_cust_id = qbo_check_customer(sc)

    return "abc"

################################################################################### CHECK QUICKBOOKS CUSTOMER


def qbo_access_toke():
    auth_client = AuthClient(
    cfg.qbo['QBO_CLIENT_ID'],
    cfg.qbo['QBO_CLIENT_SECRET'],
    "https://tdasu.pagekite.me/redirect",
    environment="production"
    )

    scopes = [
        Scopes.ACCOUNTING,
    ]
    auth_url = auth_client.get_authorization_url(scopes)
    print(auth_url)
    return auth_url

def qbo_check_customer(ShopCustomer):
    realm_id        = cfg.qbo['realmID']
    params1         = (ShopCustomer.first_name, ShopCustomer.last_name)
    query_statement = "SELECT * FROM Customer WHERE GivenName=%s AND FamilyName=%s" % (params1)
    params2         = (realm_id, query_statement)
    base_uri        = "https://quickbooks.api.intuit.com/v3/company/%s/query?query=%s" % (params2)
    print(base_uri)

    qbo_query_id    = requests.get(base_uri)
    print(qbo_query_id)

    if not qbo_query_id['QueryResponse']:
        return qbo_create_customer()

    else:
        return qbo_query_id['QueryResponse']['Customer']['Id']

'''
################################################################################### CREATE QUICKBOOKS CUSTOMER


def qbo_create_customer():

    QboCustomer.first_name  = ShopCustomer.first_name
    QboCustomer.last_name   = ShopCustomer.last_name
    QboCustomer.email       = ShopCustomer.email
    QboCustomer.line1       = QboCustomer.first_name
    QboCustomer.line2       = ShopCustomer.address1
    QboCustomer.line3       = ShopCustomer.address2
    QboCustomer.city        = ShopCustomer.city
    QboCustomer.province    = ShopCustomer.province

    customer_body = {}

    customer_body['GivenName']                          = QboCustomer.first_name
    customer_body['FamilyName']                         = QboCustomer.last_name
    customer_body['PrimaryEmailAddr']['Address']        = QboCustomer.email
    customer_body['BillAddr']['Line1']                  = QboCustomer.line1
    customer_body['BillAddr']['Line2']                  = QboCustomer.line2
    customer_body['BillAddr']['Line3']                  = QboCustomer.line3
    customer_body['BillAddr']['City']                   = QboCustomer.city
    customer_body['BillAddr']['CountrySubDivisionCode'] = QboCustomer.province

    try:
        base_url        = configRead.get_api_url() + req_context.realm_id
        url             = base_url + '/customer' + configRead.get_minorversion(4)
        request_data    = {'payload': invoice_body, 'url': url}
        response_data   = requestMethods.request(request_data, req_context, method='POST')
        handle_response = handle_response(response_data)
    # this will have the ord
        print "Customer created successfully."

    except:
        print "Error creating customer"


    if ShopOrder.financial_status == "paid":
        return qbo_create_receipt()
    else:
        return qbo_create_invoice()


################################################################################### CREATE QUICKBOOKS INVOICE

def qbo_create_invoice():

    invoice_body = {}

    invoice_body['Invoice']['TxnDate'] = ShopOrder.date
    invoice_body['Invoice']['CustomerRef']['value'] = qbo_check_customer()

    for items in ShopOrder.lineitems:
        invoice_body['Invoice']['Line'][items]


    try:
        base_url        = configRead.get_api_url() + req_context.realm_id
        url             = base_url + '/customer' + configRead.get_minorversion(4)
        request_data    = {'payload': invoice_body, 'url': url}
        response_data   = requestMethods.request(request_data, req_context, method='POST')
        handle_response = handle_response(response_data)
        print "Invoice created successfully."

    except:
        print "Error creating invoice."


################################################################################### CREATE QUICKBOOKS RECEIPT

def qbo_create_receipt():

    receipt_body = {}

    receipt_body['GivenName'] = QboReceipt.first_name
    receipt_body['GivenName'] = QboReceipt.last_name
    receipt_body['GivenName'] = QboReceipt.email
    receipt_body['GivenName'] = QboReceipt.line1
    receipt_body['GivenName'] = QboReceipt.line2
    receipt_body['GivenName'] = QboReceipt.line3
    receipt_body['GivenName'] = QboReceipt.city
    receipt_body['GivenName'] = QboReceipt.country
    receipt_body['GivenName'] = QboReceipt.province
    receipt_body['GivenName'] = QboReceipt.postalcode


    try:
        base_url        = configRead.get_api_url() + req_context.realm_id
        url             = base_url + '/customer' + configRead.get_minorversion(4)
        request_data    = {'payload': invoice_body, 'url': url}
        response_data   = requestMethods.request(request_data, req_context, method='POST')
        handle_response = handle_response(response_data)
        print "Receipt created successfully."

    except:
        print "Error creating receipt."


################################################################################### HANDLE QUICKBOOKS RESPONSE

def handle_response(response_data):
    new_reponse = {}
    new_reponse['status_code'] = response_data['status_code']
    content = json.loads(response_data['content'])
    if response_data['status_code'] != 200:
        new_reponse['font_color'] = 'red'
        try:
            new_reponse['message'] = content['Fault']['Error'][0]['Message']
        except:
            new_reponse['message'] = "Some error occurred. Error message not found."
    else:
        new_reponse['font_color'] = 'green'
        new_reponse['message'] = "Success! Customer added to QBO"
        # More data from successful response can be retrieved like customer id
    return new_reponse
'''

################################################################################### GARBAGE

#def tests():
    # # QBO_BASE    = "sandbox-quickbooks.api.intuit.com"
    # # COMP_ID     = '123145895094094'
    # # ENT_ID      = ''
    # # QBO         = '/company/%s/customer/%s' % (COMP_ID, ENT_ID)
    # # FINAL_URL   = QBO_BASE + QBO
    # # qbo_customers = requests.get(FINAL_URL)
    # qbo_customers = json.loads(qbo)

    # customer_first_name = qbo_customers['Customer']['GivenName']

    # QBO_BASE = "https://sandbox-quickbooks.api.intuit.com"
    # qbo_select = "SELECT * FROM Customer WHERE GivenName = 'Bill'"
    # URL = "/v3/company/<realmID>/query?query=%s" % (qbo_select)
