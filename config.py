# config.py
import os
# Enable Flask's debugging features. Should be False in production
DEBUG = True


#WTForms
WTF_CSRF_ENABLED = True
SECRET_KEY = 'admin'


# Quickbooks configurations information

qbo = {
		'QBO_CLIENT_ID' 		: ""
		'QBO_CLIENT_SECRET' 	: ""
		}



# Shopify configurations information
shop = { 
		'SHOP_API_KEY' 		 : ""
		'SHOP_PASSWORD'		 : ""
		'SHOP_SHARED_SECRET' : ""
		}