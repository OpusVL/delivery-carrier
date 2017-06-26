from lxml import etree
from collections import OrderedDict


def _sub_elem(value):
    for key, val in value.items():
        if not isinstance(val, dict):
            item = key
            item.text = val
            return item
        else:
            _sub_elem(key)


def _dict_to_tnt(params):
    root = etree.Element("ESHIPPER")
    for key, val in params.items():
        item = etree.SubElement(root, key)
        if not isinstance(val, dict):
            item.text = val
        else:
            sub_item = etree.SubElement(item, _sub_elem(val))

    return etree.tostring(root, encoding='UTF-8', method='xml', standalone=False, pretty_print=True)

all_dict = OrderedDict()
all_dict.update({"LOGIN": "authentication"})
all_dict.update({"CONSIGNMENTBATCH": OrderedDict()})
all_dict.setdefault("CONSIGNMENTBATCH").update({"SENDER": "self.sender"})
all_dict.setdefault("CONSIGNMENTBATCH").update({"COLLECTION": OrderedDict()})
all_dict.setdefault("CONSIGNMENTBATCH").setdefault("COLLECTION").update({"COLLECTIONADDRESS": "self.sender"})
all_dict.setdefault("CONSIGNMENTBATCH").setdefault("COLLECTION").update({"SHIPDATE": "12/05/2017"})
all_dict.setdefault("CONSIGNMENTBATCH").setdefault("COLLECTION").update({"PREFCOLLECTTIME": "preftime"})
all_dict.setdefault("CONSIGNMENTBATCH").setdefault("COLLECTION").update({"ALTCOLLECTTIME": "alttime"})
all_dict.setdefault("CONSIGNMENTBATCH").update({"CONSIGNMENT": OrderedDict()})
all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").update({"CONREF": "CONREF"})
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
all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"INSURANCEVALUE": ""})
all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update(
    {"INSURANCECURRENCY": ""})
all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"SERVICE": ""})
all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"OPTION": ""})
all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"DESCRIPTION": ""})
all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"DELIVERYINST": ""})
all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update(
    {"PACKAGE": OrderedDict()})
all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").setdefault("PACKAGE").update(
    {"ITEMS": ""})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").setdefault("PACKAGE").update({"DESCRIPTION": ""})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").setdefault("PACKAGE").update({"LENGTH": ""})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").setdefault("PACKAGE").update({"HEIGHT": ""})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").setdefault("PACKAGE").update({"WIDTH": ""})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").setdefault("PACKAGE").update({"WEIGHT": ""})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").setdefault("PACKAGE").update({"ARTICLE": OrderedDict()})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").setdefault("PACKAGE").setdetault("ARTICLE").update({"ITEMS": ""})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").setdefault("PACKAGE").setdetault("ARTICLE").update({"DESCRIPTION": ""})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").setdefault("PACKAGE").setdetault("ARTICLE").update({"WEIGHT": ""})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").setdefault("PACKAGE").setdetault("ARTICLE").update({"INVOICEVALUE": ""})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").setdefault("PACKAGE").setdetault("ARTICLE").update({"INVOICEDESC": ""})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").setdefault("PACKAGE").setdetault("ARTICLE").update({"HTS": ""})
# all_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").setdefault("PACKAGE").setdetault("ARTICLE").update({"COUNTRY": ""})
# all_dict.update({"ACTIVITY": {"CREATE": {"CONREF": CONREF}}})
# all_dict.setdefault("ACTIVITY").update({"RATE": {"CONREF": CONREF}})
# all_dict.setdefault("ACTIVITY").update({"BOOK": {"CONREF": CONREF}})
# all_dict.setdefault("ACTIVITY").update({"SHIP": {"CONREF": CONREF}})
# all_dict.setdefault("ACTIVITY").update({"PRINT": OrderedDict})
# all_dict.setdefault("ACTIVITY").setdefault("PRINT").update({"CONNOTE": {"CONREF": CONREF}})
# all_dict.setdefault("ACTIVITY").setdefault("PRINT").update({"LABEL": {"CONREF": CONREF}})
# all_dict.setdefault("ACTIVITY").setdefault("PRINT").update({"MANIFEST": {"CONREF": CONREF}})
# all_dict.setdefault("ACTIVITY").setdefault("PRINT").update({"INVOICE": {"CONREF": CONREF}})
# all_dict.setdefault("ACTIVITY").setdefault("PRINT").update({"EMAILFROM": {"CONREF": CONREF}})
# all_dict.setdefault("ACTIVITY").setdefault("PRINT").update({"EMAILTO": {"CONREF": CONREF}})
# all_dict.setdefault("ACTIVITY").update({"ACTIVITY": None})

xml_data = _dict_to_tnt(all_dict)
print xml_data
