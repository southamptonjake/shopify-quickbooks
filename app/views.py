from app import app
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector as mariadb
import json, jsonify, collections, itertools, csv
import requests
import config as cfg
import models



################################################################################### SHOPIFY ORDER WEBHOOK

def get_new_order():

    # this will have the order
    # payload = request.get_data()
    payload = json.load(open('objects/shop_order_webhook.json'))
    
    ShopOrder.id                = payload['id']
    ShopOrder.date              = payload['created_at']
    ShopOrder.total_price       = payload['total_price']
    ShopOrder.subtotal_price    = payload['subtotal_price']
    ShopOrder.financial_status  = payload['financial_status']
    ShopOrder.total_discounts   = payload['total_discounts']
    ShopOrder.user_id           = payload['user_id']
    ShopOrder.location_id       = payload['location_id']
    ShopOrder.line_items        = payload['line_items']

    ShopCustomer.id             = payload['customer']['id']
    ShopCustomer.email          = payload['customer']['email']
    ShopCustomer.first_name     = payload['customer']['first_name'] 
    ShopCustomer.last_name      = payload['customer']['last_name']
    ShopCustomer.address1       = payload['customer']['default_address']['address1']
    ShopCustomer.address2       = payload['customer']['default_address']['address2']
    ShopCustomer.city           = payload['customer']['default_address']['city']
    ShopCustomer.province       = payload['customer']['default_address']['province']
    ShopCustomer.phone          = payload['customer']['default_address']['phone']

    for items in payload['line_items']:

        OrderItems.id               = item['id']
        OrderItems.title            = item['title']
        OrderItems.quantity         = item['quantity']
        OrderItems.price            = item['price']
        OrderItems.sku              = item['sku']
        OrderItems.product_id       = item['product_id']
        OrderItems.total_discount   = item['total_discount']

    return check_customer()


################################################################################### CHECK QUICKBOOKS CUSTOMER

def qbo_check_customer():

    if not payload['customer']['first_name']:
        
        return qbo_create_fake_customer()
    
    else

        realm_id        = cfg.qbo['realmID']
        params1         = (ShopCustomer.first_name, ShopCustomer.last_name)
        query_statement = "SELECT * FROM Customer WHERE GivenName=%s AND FamilyName=%s" % (params1)
        params2         = (realm_id, query_statement)
        base_uri        = "https://quickbooks.api.intuit.com/v3/company/%s/query?query=%s" % (params2)

        qbo_query_id    = requests.get(base_uri)
        qbo_query_id    = qbo_query.json()

        if not qbo_query_id['QueryResponse']:
            return qbo_create_customer()
        
        else:
            return customer_id = qbo_query_id['QueryResponse']['Customer']['Id']:


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
        print "Customer created successfully."

    except:
        print "Error creating customer"


    if ShopOrder.financial_status == "paid"
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


################################################################################### GARBAGE

def tests():
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

