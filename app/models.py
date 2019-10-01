

################################################################################### SHOPIFY OBJECTS
#Shopify Order object
class ShopOrder:
    def __init__(self, total_price,line_items):
        self.total_price = total_price
        self.line_items = line_items


#Shopify Customer object
class ShopCustomer:
    def __init__(self,email,first_name,last_name,phone,company,address1,address2,city,post_code,):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.company = company

        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.post_code = post_code



#Shopify Items in Order object
class ShopOrderItem:
    def __init__(self, title, quantity, price, sku):
        self.title = title
        self.quantity = quantity
        self.price = price
        self.sku = sku
        self.quickbooks_id = -1



################################################################################### QUICKBOOKS OBJECTS

# Customer object
class QboCustomer:
    def __init__(self, entity_id, first_name, last_name, email, address1, address2, city, province):
        self.entity_id      = entity_id
        self.first_name     = first_name
        self.family_name    = last_name
        self.email          = email
        self.address1       = line1
        self.address2       = line2
        self.address3       = line3
        self.city           = city
        self.country        = country
        self.province       = estate
        self.postalcode     = postalcode
