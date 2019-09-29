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
from quickbooks.objects.base import Address,EmailAddress,PhoneNumber
import pickle
from quickbooks.objects import Invoice,SalesItemLineDetail,SalesItemLine

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
    qbo_create_invoice(so,quickbooks_cust_id)
    return "abc"

################################################################################### CHECK QUICKBOOKS CUSTOMER

def qbo_check_customer(sc):
    client = create_qbc()
    customers = Customer.filter(Active=True, FamilyName=sc.last_name, GivenName=sc.first_name, qb=client)
    if(len(customers) == 0):
        return qbo_create_customer(sc)
    else:
        return customers[0].Id


################################################################################### CREATE QUICKBOOKS CUSTOMER

def qbo_create_customer(sc):
    client = create_qbc()

    customer = Customer()
    customer.GivenName = sc.first_name
    customer.FamilyName = sc.last_name
    customer.CompanyName = sc.company

    phone = PhoneNumber()
    phone.FreeFormNumber = sc.phone
    customer.PrimaryPhone = phone

    email = EmailAddress()
    email.Address = sc.email
    customer.PrimaryEmailAddr = email

    address = Address()
    address.Line1 = sc.address1
    address.Line2 = sc.address2
    address.City = sc.city
    address.PostalCode = sc.post_code
    customer.BillAddr = address

    customer.save(qb=client)
    return customer.Id


################################################################################### CREATE QUICKBOOKS INVOICE

def qbo_create_invoice(so, customer_id):

    client = create_qbc()
    customer_ref = Customer.get(customer_id, qb=client).to_ref()
    print(customer_ref)
    line_detail = SalesItemLineDetail()
    line_detail.UnitPrice = 100  # in dollars
    line_detail.Qty = 1  # quantity can be decimal

    line = SalesItemLine()
    line.Amount = 100  # in dollars
    line.SalesItemLineDetail = line_detail

    item_ref = Ref()
    item_ref = so.


    invoice = Invoice()
    invoice.CustomerRef = customer_ref
    invoice.Line = [line]

    invoice.save(qb=client)


def create_qbc():


    refresh_token = pickle.load( open( "refresh.token", "rb" ) )
    realm_id = pickle.load( open( "realm.id", "rb" ) )
    auth_client = AuthClient(
    cfg.qbo['QBO_CLIENT_ID'],
    cfg.qbo['QBO_CLIENT_SECRET'],
    "https://tdasu.pagekite.me/redirect",
    environment="production"
    )
    client = QuickBooks(
        auth_client=auth_client,
        refresh_token=refresh_token,
        company_id=realm_id,
    )
    return client

@app.route("/redirect")
def redirect():
    auth_client = AuthClient(
    cfg.qbo['QBO_CLIENT_ID'],
    cfg.qbo['QBO_CLIENT_SECRET'],
    "https://tdasu.pagekite.me/redirect",
    environment="production"
    )
    auth_client.get_bearer_token(request.args.get('code'), realm_id=request.args.get('realmId'))
    pickle.dump(auth_client.refresh_token, open( "refresh.token", "wb" ) )
    pickle.dump(request.args.get('realmId'), open( "realm.id", "wb" ) )
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
