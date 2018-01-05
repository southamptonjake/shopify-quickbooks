# shopify-quickbooks

I've always been really frustrated for not being able to control my Accounts Receivable (of Shopify created orders) with Quickbooks.
Apps are either expensive (~USD 30/month) or don't work correctly.
This is an effort to integrate Shopify and Quickbooks, starting with the basics: an order created in Shopify creates a Invoice/Receipt in Quickbooks.

The mid-level logic is:

**1. Order is created on Shopify**

  a. Subscribe to Webhook notification to Shopify to receive new orders created.
  
  b. Parse information to organize the order contents in each respective class.
  
The function `get_new_order()` get's the JSON object and parses it into different fields.
Folder /objects/shop_order_webhook.json contains an example of the type of load that is received.


**2. Check whether the Shopify Customer that placed the order already exhists in Quickbooks**

The function `qbo_check_customer()` queries QBO database to check whether the customer that placed an order on Shopify
already exhists in the QBO database. If it doesn't exhists goes to `qbo_create_customer` function.
If the does, get's the customer ID (important to be able to create the invoice/receipt).


**3. Creates a customer**

The function `qbo_create_customer()` get's each relevant field from the order and parses it into the specific QBO fields.
It then dumps the object to QBO API, and for the next step, checks whether the order has been paid or not.
If it has, creates a `Receipt`, if it hasn't, creates an `Invoice`.


**4a. Creates an Invoice**

Folder /objects/qbo_invoice.json contains an example of the structure of the invoice object.
Creates an invoice and dumps it into the QBO API. An invoice has to have a Customer ID (CustomerRef for the Invoice Object),
so it grabs the id of the cliente via the `qbo_check_customer`.


**4b. Creates an Receipt**

Folder /objects/qbo_receipt.json contains an example of the structure of the receipt object.
Similar logic as the invoice function.


**This is, and always will be an open source project.**
**The objective is to make it run smoothly and to publish it for free in the AppStore of both applications**

