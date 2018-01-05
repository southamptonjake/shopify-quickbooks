

################################################################################### SHOPIFY OBJECTS
#Shopify Order object
class ShopOrder:
    def __init__(self, id, total_price, subtotal_price, financial_status, total_discounts, user_id, location_id, line_items):
        self.id
        self.total_price
        self.subtotal_price
        self.financial_status
        self.total_discounts
        self.user_id
        self.location_id
        self.line_items


#Shopify Customer object
class ShopCustomer:
    def __init__(self, f_name, l_name, m_name, phone, email):
        self.id             = id
        self.email          = email
        self.first_name     = first_name
        self.last_name      = last_name
        self.address1       = address1
        self.address2       = address2
        self.city           = city
        self.province       = province
        self.phone          = phone




#Shopify Items in Order object
class ShopOrderItems:
    def __init__(self, id, title, quantity, price, sku, product_id, total_discount):
        self.id
        self.title
        self.quantity
        self.price
        self.sku
        self.product_id
        self.total_discount



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



# Invoice object
class QBOSalesInvoice:
    def __init__(self, f_name, l_name, m_name, phone, email):
        self.given_name = f_name
        self.middle_name = m_name
        self.family_name = l_name
        self.primary_phone = phone
        self.primary_email_addr = email



# Receipt object
class QBOSalesReceipt:
	def __init__(self, f_name, l_name, m_name, phone, email):
        self.given_name = f_name
        self.middle_name = m_name
        self.family_name = l_name
        self.primary_phone = phone
        self.primary_email_addr = email



# Payment (received) object
class QBOPayment:
	def __init__(self, f_name, l_name, m_name, phone, email):
        self.given_name = f_name
        self.middle_name = m_name
        self.family_name = l_name
        self.primary_phone = phone
        self.primary_email_addr = email

