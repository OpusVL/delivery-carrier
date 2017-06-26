from lxml import etree
from collections import OrderedDict


# The receiver address details
# ADDRESS_MAPPING = {
#     'COMPANYNAME': "consignee_name",
#     # 'T8906': "contact",
#     'STREETADDRESS1': "street",
#     'STREETADDRESS2': "street2",
#     'STREETADDRESS3': "street3",
#     'POSTCODE': "zip",
#     'CITY': "city",
#     'COUNTRY': "country_code",
#     'CONTACTTELEPHONE': "consignee_phone",
#     # 'T1230': "consignee_mobile",
#     'CONTACTEMAIL': "consignee_email",
# }
# PARCEL_MAPPING = {
#     'T530': "weight",
#     'T8973': "parcel_number_barcode",
#     'T8904': "parcel_number_label",
# }
# DELIVERY_MAPPING = {
#     # 'address': ADDRESS_MODEL,
#     'T859': "consignee_ref",
#     'T854': "additional_ref_1",
#     'T8907': "additional_ref_1",
#     'T8908': "additional_ref_2",
#     'T540': "shipping_date",
#     'T8318': "commentary",
#     'T8975': "tnt_origin_reference",
#     'T8905': "parcel_total_number",
#     'T8702': "parcel_total_number",
# }

# The sender details
# ACCOUNT_MAPPING = {
#     # 'COMPANYNAME': "customer_id",
#     'CONTACTNAME': "contact_id",
#     # 'T8700': "outbound_depot",
#     'STREETADDRESS1': "shipper_street",
#     'COMPANYNAME': "shipper_name",
#     'POSTCODE': "shipper_zip",
#     'CITY': "shipper_city",
#     'COUNTRY': "shipper_country",
# }

# TNT Authentication. Requires parent node LOGIN
AUTHENTICATION_MAPPING = OrderedDict(
    COMPANY="",
    PASSWORD="",
    APPID="IN",
    APPVERSION="2.2"
)

CONREF = ""

COLLECTION_ADDRESS_MAPPING = OrderedDict(
    COMPANYNAME="",
    STREETADDRESS1="",
    STREETADDRESS2="",
    STREETADDRESS3="",
    CITY="",
    PROVINCE="",
    POSTCODE="",
    COUNTRY="",
    VAT="",
    CONTACTNAME="",
    CONTACTDIALCODE="",
    CONTACTTELEPHONE="",
    CONTACTEMAIL="",
)

PREFCOLLECTTIME_MAPPING = OrderedDict(
    FROM="",
    TO=""
)

ALTCOLLECTTIME_MAPPING = OrderedDict(
    FROM="",
    TO=""
)

# TNT Sender details. Requires parent node CONSIGNMENTBATCH
SENDER_MAPPING = OrderedDict(
    COMPANYNAME="contact_id",
    STREETADDRESS1="",
    STREETADDRESS2="",
    STREETADDRESS3="",
    CITY="",
    PROVINCE="",
    POSTCODE="",
    COUNTRY="",
    ACCOUNT="",
    VAT="",
    CONTACTNAME="",
    CONTACTDIALCODE="",
    CONTACTTELEPHONE="",
    CONTACTEMAIL="",
    COLLECTION=OrderedDict(
        COLLECTIONADDRESS=COLLECTION_ADDRESS_MAPPING,
        SHIPDATE="",
        PREFCOLLECTTIME=PREFCOLLECTTIME_MAPPING,
        ALTCOLLECTTIME=ALTCOLLECTTIME_MAPPING,
        COLLINSTRUCTIONS=""
    )
)

RECEIVER_MAPPING = OrderedDict(
    COMPANYNAME="",
    STREETADDRESS1="",
    STREETADDRESS2="",
    STREETADDRESS3="",
    CITY="",
    PROVINCE="",
    POSTCODE="",
    COUNTRY="",
    VAT="",
    CONTACTNAME="",
    CONTACTDIALCODE="",
    CONTACTTELEPHOPNE="",
    CONTACTEMAIL="",
)

DELIVERY_MAPPING = OrderedDict(
    COMPANYNAME="",
    STREETADDRESS1="",
    STREETADDRESS2="",
    STREETADDRESS3="",
    CITY="",
    PROVINCE="",
    POSTCODE="",
    COUNTRY="",
    VAT="",
    CONTACTNAME="",
    CONTACTDIALCODE="",
    CONTACTTELEPHOPNE="",
    CONTACTEMAIL="",
)

PACKAGE_MAPPING = OrderedDict(
    ITEMS="",
    DESCRIPTION="",
    LENGTH="",
    HEIGHT="",
    WIDTH="",
    WEIGHT="",

)

DETAILS_MAPPING = OrderedDict(
    RECEIVER=RECEIVER_MAPPING,
    DELIVERY=DELIVERY_MAPPING,
    CUSTOMERREF="",
    CONTYPE="",
    PAYMENT="",
    ITEMS="",
    TOTALWEIGHT="",
    TOTALVOLUME="",
    CURRENCY="",
    GOODSVALUE="",
    INSURANCEVALUE="",
    INSURANCECURRENCY="",
    SERVICE="",
    OPTION="",
    DESCRIPTION="",
    DELIVERYINST="",
    PACKAGE=PACKAGE_MAPPING,
)

ACTIVITY_MAPPING = OrderedDict(
    CREATE=OrderedDict(
        CONREF=CONREF
    ),
    RATE=OrderedDict(
        CONREF=CONREF
    ),
    BOOK=OrderedDict(
        CONREF=CONREF
    ),
    SHIP=OrderedDict(
        CONREF=CONREF
    ),
    PRINT=OrderedDict(
        CONNOTE=OrderedDict(
            CONREF=CONREF
        ),
        LABEL=OrderedDict(
            CONREF=CONREF
        ),
        MANIFEST=OrderedDict(
            CONREF=CONREF
        ),
        INVOICE=OrderedDict(
            CONREF=CONREF
        ),
        EMAILTO="",
        EMAILFROM=""
    ),
    SHOW_GROUPCODE=""
)


all_dict = OrderedDict(
    LOGIN=AUTHENTICATION_MAPPING,
    CONSIGNMENTBATCH=OrderedDict(
        SENDER=SENDER_MAPPING,
        CONSIGNMENT=OrderedDict(
            CONREF=CONREF,
            DETAILS=DETAILS_MAPPING
            )
        ),
    ACTIVITY=ACTIVITY_MAPPING
    )

# all_dict = {
#     "LOGIN": {},
#     "CONSIGNMENTBATCH": {"SENDER": CONSIGNMENT_MAPPING},
#     "ACTIVITY": {},
# }
# all_dict.setdefault("LOGIN").update(AUTHENTICATION_MAPPING)
# all_dict.setdefault("CONSIGNMENTBATCH").update(CONSIGNMENT_MAPPING)
# all_dict.update(DELIVERY_MAPPING)
# all_dict.update(ADDRESS_MAPPING)


def dict_to_tnt_data(params):
    root = etree.Element('ESHIPPER')

    for key, val in params.items():
        item = etree.SubElement(root, key)
        if not isinstance(val, dict):
            item.text = val
        else:
            for key2, val2 in val.items():
                item2 = etree.SubElement(item, key2)
                if not isinstance(val2, dict):
                    item2.text = val2
                else:
                    for key3, val3 in val2.items():
                        item3 = etree.SubElement(item2, key3)
                        if not isinstance(val3, dict):
                            item3.text = val3

    return etree.tostring(root, encoding='UTF-8', method='xml', standalone=False, pretty_print=True)

print dict_to_tnt_data(all_dict)
