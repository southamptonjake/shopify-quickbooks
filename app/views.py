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
from quickbooks.objects.item import Item
from quickbooks.objects.account import Account

from quickbooks.objects.base import Address,EmailAddress,PhoneNumber,Ref
import pickle
from quickbooks.objects import Invoice,SalesItemLineDetail,SalesItemLine

@app.route("/")
def index():
    client = create_qbc()
    item = Item()
    item.Name = "test"
    item.UnitPrice = 100
    item.Type = "Service"

    item.save(qb=client)
    return item.Id

################################################################################### SHOPIFY ORDER WEBHOOK

@app.route("/shopifyorder",methods = ['POST','GET'])
def get_new_order():

    # this will have the order
    #payload = request.json
    payload = json.load(open('app/objects/shop_order_webhook.json'))



    cust_hold = payload['customer']
    address_hold = cust_hold['default_address']
    sc = models.ShopCustomer(cust_hold['email'],cust_hold['first_name'], cust_hold['last_name'], cust_hold['phone'],address_hold['company'],address_hold['address1'],address_hold['address2'],address_hold['city'],address_hold['zip'])

    ois = []

    for item in payload['line_items']:
        oi = models.ShopOrderItem(item['title'],item['quantity'],item['price'],item['sku'])
        ois.append(oi)



    print(sc.email)
    quickbooks_cust_id = qbo_check_customer(sc)
    print(quickbooks_cust_id)

    for item in ois:
        item.quickbooks_id = qbo_check_item(item)
        print(item.quickbooks_id)

    so = models.ShopOrder(payload['total_price'],ois)

    qbo_create_invoice(so,quickbooks_cust_id)
    return "abc"

################################################################################### CHECK QUICKBOOKS CUSTOMER

def qbo_find_sales_account():
    client = create_qbc()
    account = Customer.filter(Active=True, Name="Sales", qb=client)
    return account[0].Id


def qbo_check_customer(sc):
    client = create_qbc()
    customers = Customer.filter(Active=True, FamilyName=sc.last_name, GivenName=sc.first_name, qb=client)
    if(len(customers) == 0):
        return qbo_create_customer(sc)
    else:
        return customers[0].Id

def qbo_check_item(soi):
    client = create_qbc()
    items = Item.filter(Active=True, Sku=soi.sku, qb=client)
    if(len(items) == 0):
        items = Item.filter(Active=True, Name=soi.title, qb=client)
        if(len(items) == 0):
            return qbo_create_item(soi)
        else:
            return items[0].Id
    else:
        return items[0].Id



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

################################################################################### CREATE QUICKBOOKS Item

def qbo_create_item(soi):
    client = create_qbc()
    item = Item()

    print(soi.title)
    print(soi.price)

    item.Name = soi.title
    item.UnitPrice = soi.price
    item.Type = "Service"
    item.Sku = soi.sku

    account = Account.filter(Active=True, Name="Sales", qb=client)
    account_ref = Account.get(account[0].Id, qb=client).to_ref()

    item.IncomeAccountRef = account_ref
    item.save(qb=client)
    return item.Id


################################################################################### CREATE QUICKBOOKS INVOICE

def qbo_create_invoice(so, customer_id):

    client = create_qbc()

    customer_ref = Customer.get(customer_id, qb=client).to_ref()

    line_detail = SalesItemLineDetail()
    line_detail.UnitPrice = 100  # in dollars
    line_detail.Qty = 1  # quantity can be decimal

    item_ref = Item.get(35, qb=client).to_ref()
    line_detail.ItemRef = item_ref

    line = SalesItemLine()
    line.Amount = 100  # in dollars
    line.SalesItemLineDetail = line_detail
    line.DetailType = "SalesItemLineDetail"

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
