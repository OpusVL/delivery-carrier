# from xml.etree import cElementTree as Et
from lxml import etree, html

root = etree.Element('ESHIPPER')

login = etree.SubElement(root, 'LOGIN')

company = etree.SubElement(login, 'COMPANY')
company.text = 'username'

password = etree.SubElement(login, 'PASSWORD')
password.text = 'password'

app_id = etree.SubElement(login, 'APPID')
app_id.text = 'IN'

app_ver = etree.SubElement(login, 'APPVERSION')
app_ver.text = '2.2'

consignment = etree.SubElement(root, 'CONSIGNMENTBATCH')
sender = etree.SubElement(consignment, 'SENDER')

company_name = etree.SubElement(sender, 'COMPANYNAME')
company_name.text = 'Company Name'
street_address_1 = etree.SubElement(sender, 'STREETADDRESS1')
street_address_1.text = 'First Address'
street_address_2 = etree.SubElement(sender, 'STREETADDRESS2')
street_address_2.text = 'Second Address'
street_address_3 = etree.SubElement(sender, 'STREETADDRESS3')
street_address_3.text = 'Third Address'
city = etree.SubElement(sender, 'CITY')
city.text = 'City'
province = etree.SubElement(sender, 'PROVINCE')
province.text = 'County'
post_code = etree.SubElement(sender, 'POSTCODE')
post_code.text = 'CV21 XXX'
country = etree.SubElement(sender, 'COUNTRY')
country.text = 'United Kingdom'
account = etree.SubElement(sender, 'ACCOUNT')
account.text = '1234567890'
vat = etree.SubElement(sender, 'VAT')
contact_name = etree.SubElement(sender, 'CONTACTNAME')
contact_name.text = 'John Doe'
contact_dialcode = etree.SubElement(sender, 'CONTACTDIALCODE')
contact_dialcode.text = '01788'
contact_telephone = etree.SubElement(sender, 'CONTACTTELEPHONE')
contact_telephone.text = '815648'
contact_email = etree.SubElement(sender, 'CONTACTEMAIL')
contact_email.text = 'my@email.com'

collection = etree.SubElement(sender, 'COLLECTION')

ship_date = etree.SubElement(collection, 'SHIPDATE')
ship_date.text = '15/08/2017'
pref_collection_time = etree.SubElement(collection, 'PREFCOLLECTTIME')
pref_collection_from = etree.SubElement(pref_collection_time, 'FROM')
pref_collection_from.text = '09:00'
pref_collection_to = etree.SubElement(pref_collection_time, 'TO')
pref_collection_to.text = '10:00'
alt_collection_time = etree.SubElement(collection, 'ALTCOLLECTTIME')
alt_collection_from = etree.SubElement(alt_collection_time, 'FROM')
alt_collection_from.text = '11:00'
alt_collection_to = etree.SubElement(alt_collection_time, 'TO')
alt_collection_to.text = '12:00'
collection_instructions = etree.SubElement(collection, 'COLLINSTRUCTIONS')
collection_instructions.text = 'Leave at side door'

print etree.tostring(root, encoding='UTF-8', method='xml', standalone=False, pretty_print=True)

# elements = [login, consignment]
# xml_string = ''

# for elem in elements:
#     xml_string += etree.tostring(elem)
#
# print xml_string

# output_initial = str(etree.tostring(login, encoding='UTF-8', method='xml', standalone=True))

# print html.tostring(collection, pretty_print=True)

# final_output = str(output_initial) += str(html.tostring(collection))
# encoding='UTF-8', method='xml', standalone=False, pretty_print=True