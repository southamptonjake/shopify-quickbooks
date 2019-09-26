from app import app
from flask import Flask, render_template, request, redirect, url_for, session
import json, jsonify, collections, itertools, csv
import requests
import config as cfg
from . import models
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
import re
from quickbooks import QuickBooks
from quickbooks.objects.customer import Customer
from quickbooks.objects.base import Address

@app.route("/")
def index():
    client = create_qbc()
    customers = Customer.all(qb=client)
    print(customers[30])
    return "1"

################################################################################### SHOPIFY ORDER WEBHOOK

@app.route("/shopifyorder",methods = ['POST','GET'])
def get_new_order():

    # this will have the order
    #payload = request.json
    payload = json.load(open('app/objects/shop_order_webhook.json'))

    so = models.ShopOrder(payload['total_price'],payload['subtotal_price'],payload['financial_status'],payload['total_discounts'],
    payload['user_id'],payload['location_id'],payload['line_items'])

    cust_hold = payload['customer']
    address_hold = cust_hold['default_address']
    sc = models.ShopCustomer(cust_hold['email'],cust_hold['first_name'], cust_hold['last_name'], cust_hold['phone'],address_hold['company'],address_hold['address1'],address_hold['address2'],address_hold['city'],address_hold['zip'])

    ois = []

    for item in payload['line_items']:
        oi = models.ShopOrderItems(item['title'],item['quantity'],item['price'],item['sku'],item['product_id'], item['total_discount'])
        ois.append(oi)

    print(sc.email)
    quickbooks_cust_id = qbo_check_customer(sc)
    print(quickbooks_cust_id)
    return "abc"

################################################################################### CHECK QUICKBOOKS CUSTOMER

def qbo_check_customer(sc):
    client = create_qbc()
    customers = Customer.filter(Active=True, FamilyName=sc.last_name, GivenName=sc.first_name, qb=client)
    if(len(customers) == 0):
        return qbo_create_customer(sc)
    else:
        return customers[0].Id

    #if not qbo_query_id['QueryResponse']:
    #

    #else:
    #    return qbo_query_id['QueryResponse']['Customer']['Id']


################################################################################### CREATE QUICKBOOKS CUSTOMER


def qbo_create_customer(sc):
    client = create_qbc()

    customer = Customer()
    customer.GivenName = sc.first_name
    customer.FamilyName = sc.last_name
    customer.primary_phone = sc.phone
    customer.PrimaryEmailAddr = sc.email
    customer.CompanyName = sc.company

    address = Address()
    address.Line1 = sc.address1
    address.Line2 = sc.address2
    address.City = sc.city
    address.PostalCode = sc.post_code

    customer.BillAddr = address

    customer.save(qb=client)
    return customer.Id

'''
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

def create_qbc():
    auth_client = AuthClient(
    cfg.qbo['QBO_CLIENT_ID'],
    cfg.qbo['QBO_CLIENT_SECRET'],
    "https://tdasu.pagekite.me/redirect",
    environment="production"
    )
    client = QuickBooks(
        auth_client=auth_client,
        refresh_token=session['refresh_token'],
        company_id=session["realm_id"],
    )
    return client

@app.route("/redirect")
def redirect():

    session["auth_code"] = request.args.get('code')
    session["realm_id"] =  request.args.get('realmId')
    auth_client = AuthClient(
    cfg.qbo['QBO_CLIENT_ID'],
    cfg.qbo['QBO_CLIENT_SECRET'],
    "https://tdasu.pagekite.me/redirect",
    environment="production"
    )
    auth_client.get_bearer_token(session["auth_code"], realm_id=session["realm_id"])
    session['access_token'] = auth_client.access_token
    session['refresh_token'] = auth_client.refresh_token
    return "set up"

@app.route("/startup")
def start_up():
    auth_client = AuthClient(
    cfg.qbo['QBO_CLIENT_ID'],
    cfg.qbo['QBO_CLIENT_SECRET'],
    "https://tdasu.pagekite.me/redirect",
    environment="production"
    )

    scopes = [
        Scopes.ACCOUNTING,
        Scopes.PROFILE,
        Scopes.EMAIL,
        Scopes.OPENID,
        Scopes.ADDRESS,
        Scopes.PHONE
    ]
    auth_url = auth_client.get_authorization_url(scopes)
    print(auth_url)
    result = "<a href=\"" + auth_url + "\">" + auth_url + "</a"
    return result

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
