from collections import OrderedDict

import lxml.etree as et


AUTHENTICATION = OrderedDict()
AUTHENTICATION.update({"COMPANY": "AMSBIO"})
AUTHENTICATION.update({"PASSWORD": "password"})
AUTHENTICATION.update({"APPID": "IN"})
AUTHENTICATION.update({"APPVERSION": "2.2"})

SENDER = OrderedDict()
SENDER.update({"COMPANYNAME": "Company Name"})
SENDER.update({"STREETADDRESS1": "Street 1"})
SENDER.update({"STREETADDRESS2": "Street 2"})
SENDER.update({"STREETADDRESS3": "Street 3"})
SENDER.update({"CITY": "City"})
SENDER.update({"PROVINCE": "Warks"})
SENDER.update({"POSTCODE": "CV21"})
SENDER.update({"COUNTRY": "GB"})
SENDER.update({"ACCOUNT": "987654321"})
SENDER.update({"VAT": ""})
SENDER.update({"CONTACTNAME": "Name"})
SENDER.update({"CONTACTDIALCODE": "None"})
SENDER.update({"CONTACTTELEPHONE": "07777"})
SENDER.update({"CONTACTEMAIL": "name@email.com"})


all_dict = OrderedDict()
all_dict.update({"LOGIN": AUTHENTICATION})
all_dict.update({"CONSIGNMENTBATCH": OrderedDict()})
all_dict.setdefault("CONSIGNMENTBATCH").update({"SENDER": SENDER})
all_dict.setdefault("CONSIGNMENTBATCH").setdefault("SENDER").update({"COLLECTION": OrderedDict()})
all_dict.setdefault("CONSIGNMENTBATCH").setdefault("SENDER").setdefault("COLLECTION").update({"COLLECTIONADDRESS": SENDER})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("SENDER").setdefault("COLLECTION").update({"SHIPDATE": "12/05/2017"})
# # all_dict.setdefault("CONSIGNMENTBATCH").setdefault("SENDER").setdefault("COLLECTION").update({"PREFCOLLECTTIME": preftime})
# # all_dict.setdefault("CONSIGNMENTBATCH").setdefault("SENDER").setdefault("COLLECTION").update({"ALTCOLLECTTIME": alttime})
# all_dict.setdefault("CONSIGNMENTBATCH").update({"CONSIGNMENT": OrderedDict()})
# # all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").update({"CONREF": CONREF})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").update({"DETAILS": OrderedDict()})
# # all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"RECEIVER": address})
# # all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"DELIVERY": address})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"CUSTOMREF": ""})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"CONTYPE": ""})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"PAYMENTIND": ""})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"ITEMS": ""})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"TOTALWEIGHT": ""})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"TOTALVOLUME": ""})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"CURRENCY": ""})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"GOODSVALUE": ""})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"INSURANCEVALUE": ""})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update(
#     {"INSURANCECURRENCY": ""})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"SERVICE": ""})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"OPTION": ""})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"DESCRIPTION": ""})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"DELIVERYINST": ""})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update(
#     {"PACKAGE": OrderedDict()})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").setdefault("PACKAGE").update(
#     {"ITEMS": ""})


# print data2xml(all_dict)

def recursion(data, root=None):
    if root is None:
        root = et.Element("ESHIPPER")
    else:
        et.SubElement(root, data)