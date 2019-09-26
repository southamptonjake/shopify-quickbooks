

################################################################################### SHOPIFY OBJECTS
#Shopify Order object
class ShopOrder:
    def __init__(self, total_price, subtotal_price, financial_status, total_discounts, user_id, location_id, line_items):
        self.total_price = total_price
        self.subtotal_price = subtotal_price
        self.financial_status = financial_status
        self.total_discounts = total_discounts
        self.user_id = user_id
        self.location_id = location_id
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
class ShopOrderItems:
    def __init__(self, title, quantity, price, sku, product_id, total_discount):
        self.title = title
        self.quantity = quantity
        self.price = price
        self.sku = sku
        self.product_id = product_id
        self.total_discount = total_discount



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
