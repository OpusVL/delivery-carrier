# -*- coding: utf-8 -*-
from lxml import etree
from collections import OrderedDict


AUTHENTICATION = OrderedDict()
AUTHENTICATION.update({"COMPANY": "AMSBIO"})
AUTHENTICATION.update({"PASSWORD": "password"})
AUTHENTICATION.update({"APPID": "IN"})
AUTHENTICATION.update({"APPVERSION": "2.2"})

SENDER = OrderedDict()
SENDER.update({"COMPANYNAME": "My Company"})
SENDER.update({"STREETADDRESS1": "My Street"})
SENDER.update({"STREETADDRESS2": "My Street 2"})
SENDER.update({"STREETADDRESS3": "My Street 3"})
SENDER.update({"CITY": "My City"})
SENDER.update({"PROVINCE": "Warks"})
SENDER.update({"POSTCODE": "CV21"})
SENDER.update({"COUNTRY": "GB"})
SENDER.update({"ACCOUNT": "987654321"})
SENDER.update({"VAT": None})
SENDER.update({"CONTACTNAME": "My Name"})
SENDER.update({"CONTACTDIALCODE": "None"})
SENDER.update({"CONTACTTELEPHONE": "1234567890"})
SENDER.update({"CONTACTEMAIL": "name@email.com"})


PREFTIME = OrderedDict()
PREFTIME.update({"PREFTIME_FROM": "10:00"})
PREFTIME.update({"PREFTIME_TO": "11:00"})

ALTTIME = OrderedDict()
ALTTIME.update({"ALTTIME_FROM": "12:00"})
ALTTIME.update({"ALTTIME_TO": "13:00"})



def main():
    all_dict = OrderedDict()
    all_dict.update({"LOGIN": AUTHENTICATION})
    all_dict.update({"CONSIGNMENTBATCH": OrderedDict()})
    all_dict.setdefault("CONSIGNMENTBATCH").update({"SENDER": SENDER})
    all_dict.setdefault("CONSIGNMENTBATCH").setdefault("SENDER").update({"COLLECTION": OrderedDict()})
    all_dict.setdefault("CONSIGNMENTBATCH").setdefault("SENDER").setdefault("COLLECTION").update({"COLLECTIONADDRESS": SENDER})
    all_dict.setdefault("CONSIGNMENTBATCH").setdefault("SENDER").setdefault("COLLECTION").update({"SHIPDATE": "12/05/2017"})
    all_dict.setdefault("CONSIGNMENTBATCH").setdefault("SENDER").setdefault("COLLECTION").update({"PREFCOLLECTTIME": PREFTIME})
    all_dict.setdefault("CONSIGNMENTBATCH").setdefault("SENDER").setdefault("COLLECTION").update({"ALTCOLLECTTIME": ALTTIME})
    all_dict.setdefault("CONSIGNMENTBATCH").update({"CONSIGNMENT": OrderedDict()})
    all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").update({"CONREF": "123"})
    all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").update({"DETAILS": OrderedDict()})
    # all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"RECEIVER": address})
    # all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"DELIVERY": address})
    all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"CUSTOMREF": ""})
    all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"CONTYPE": ""})
    all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"PAYMENTIND": ""})
    all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"ITEMS": ""})
    all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"TOTALWEIGHT": ""})
    all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"TOTALVOLUME": ""})
    all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"CURRENCY": ""})
    all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"GOODSVALUE": ""})
    all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update(
        {"INSURANCEVALUE": ""})
    all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update(
        {"INSURANCECURRENCY": ""})
    all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"SERVICE": ""})
    all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"OPTION": ""})
    all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"DESCRIPTION": ""})
    all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"DELIVERYINST": ""})
    all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update(
        {"PACKAGE": OrderedDict()})
    all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").setdefault(
        "PACKAGE").update(
        {"ITEMS": ""})
    root = etree.Element('ESHIPPER')
    parsed_data = recurse(root, all_dict)
    print etree.tostring(parsed_data, encoding='UTF-8', method='xml', standalone=False, pretty_print=True)


def recurse(root, data):
    for key, val in data.items():
        item = etree.SubElement(root, key)
        if not isinstance(val, dict or bool):
            item.text = val
        else:
            recurse(item, val)
    return root


if __name__ == '__main__':
    main()
