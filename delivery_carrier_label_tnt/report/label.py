# coding: utf-8
# © 2015 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import os
import httplib
import logging

import binascii
import StringIO
import pdfkit
from base64 import b64decode

import requests
from lxml import etree as et
from collections import OrderedDict
from mako.template import Template
from mako.exceptions import RichTraceback
from .label_helper import AbstractLabel
from .exception_helper import (InvalidAccountNumber)

_logger = logging.getLogger(__name__)

try:
    import pycountry
    from unidecode import unidecode
except (ImportError, IOError) as err:
    _logger.debug(err)

REPORT_CODING = 'cp1252'
ERROR_BEHAVIOR = 'backslashreplace'
REPLACEMENT_STRING = ''
TNT_PORT = 80
WEB_SERVICE_CODING = 'ISO-8859-1'
LABEL_FILE_NAME = 'tnt'

URL_PROD = "https://express.tnt.com/expressconnect/shipping/ship"
# URL_PROD = "https://express.tnt.com/expresslabel/documentation/getLabel"
# URL_TEST = "http://tnt/test/api/address"


class InvalidDataForMako(Exception):
    ""
    print "InvalidMissingField"

# def TNT_countries_prefix():
#     """For TNT carrier 'Serbie Montenegro' is 'CS' and for wikipedia it's 'ME'
#     We have to do a quick replacement
#     """
#     GLS_prefix = []
#     for elm in pycountry.countries:
#         GLS_prefix.append(str(elm.alpha_2))
#     GLS_prefix[GLS_prefix.index('ME')] = 'CS'
#     return GLS_prefix


# Update with official TNT list
EUROPEAN_COUNTRIES = [
    'AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'ES', 'EE', 'FI', 'GR',
    'GB', 'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT',
    'RO', 'SK', 'SI', 'SE']

# Here is all keys used in GLS templates
ADDRESS_MODEL = {
    "consignee_name":   {'max_size': 35, 'required': True},
    "contact":          {'max_size': 35},
    "street":           {'max_size': 35, 'required': True},
    "street2":          {'max_size': 35},
    "street3":          {'max_size': 35},
    "zip":              {'max_size': 10, 'required': True},
    "city":             {'max_size': 35, 'required': True},
    "consignee_phone":  {'max_size': 20},
    "consignee_mobile": {'max_size': 20},
    "consignee_email":  {'max_size': 100},
    # for uniship label only
    "country_norme3166": {'max_number': 999, 'min_number': 1, 'type': int},
}

AUTHENTICATION_MODEL = {
    "user_id": {"max_size": 30},
    "user_password": {"max_size": 20},
    "test_user_id": {"max_size": 30},
    "test_user_password": {"max_size": 30}
}

PARCEL_MODEL = {
    "parcel_number_label": {'max_number': 999, 'type': int, 'required': True},
    "parcel_number_barcode": {'max_number': 999, 'type': int,
                              'required': True},
    # TODO validate a weight of XX.XX (5 chars)  {0:05.2f}
    "custom_sequence": {'max_size': 10, 'min_size': 10, 'required': True},
    "weight": {'max_size': 5, 'required': True},
}
DELIVERY_MODEL = {
    # 'address': ADDRESS_MODEL,
    "consignee_ref":    {'max_size': 20},
    "additional_ref_1": {'max_size': 20},
    "additional_ref_2": {'max_size': 20},
    "shipping_date":    {'date': '%Y%m%d', 'required': True},
    "commentary":       {'max_size': 35},
    "parcel_total_number": {'max_number': 999, 'type': int, 'required': True},
}
SENDER_MODEL = {
    # "customer_id":       {'max_size': 10, 'min_size': 10, 'required': True},
    "contact_id":        {'max_size': 30},
    # "outbound_depot":    {'max_size': 6, 'min_size': 6, 'required': True},
    "shipper_name":      {'max_size': 35, 'required': True},
    "shipper_street":    {'max_size': 35, 'required': True},
    "shipper_street2":   {'max_size': 35},
    "shipper_zip":       {'max_size': 10, 'required': True},
    "shipper_city":      {'max_size': 35, 'required': True},
}

# Here is all fields called in mako template

# TNT user authentication
# AUTHENTICATION_MAPPING = {
#     'COMPANY': 'username',
#     'PASSWORD': 'password',
#     'APPID': 'IN',
#     'APPVERSION': '2.2'
# }

# The receiver address details
ADDRESS_MAPPING = {
    'COMPANYNAME': "consignee_name",
    # 'T8906': "contact",
    'STREETADDRESS1': "street",
    'STREETADDRESS2': "street2",
    'STREETADDRESS3': "street3",
    'POSTCODE': "zip",
    'CITY': "city",
    'COUNTRY': "country_code",
    'CONTACTTELEPHONE': "consignee_phone",
    # 'T1230': "consignee_mobile",
    'CONTACTEMAIL': "consignee_email",
}
PARCEL_MAPPING = {
    'T530': "weight",
    'T8973': "parcel_number_barcode",
    'T8904': "parcel_number_label",
}
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
#
# # The sender details
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
    {
        "COMPANY": "username",
        "PASSWORD": "password",
        "APPID": "app_id",
        "APPVERSION": "app_version"
    }
)

CONREF = "conref1"

COLLECTION_ADDRESS_MAPPING = OrderedDict(
    COMPANYNAME="contact_id",
    STREETADDRESS1="shipper_street",
    # STREETADDRESS2="shipper_street2",
    # STREETADDRESS3="shipper_street3",
    CITY="shipper_city",
    # PROVINCE="province",
    POSTCODE="shipper_zip",
    COUNTRY="shipper_country",
    # VAT="",
    CONTACTNAME="shipper_name",
    # CONTACTDIALCODE="",
    # CONTACTTELEPHONE="",
    # CONTACTEMAIL="",
)

PREFCOLLECTTIME_MAPPING = OrderedDict(
    FROM="preftime_from",
    TO="preftime_to"
)

ALTCOLLECTTIME_MAPPING = OrderedDict(
    FROM="alttime_from",
    TO="alttime_to"
)

# TNT Sender details. Requires parent node CONSIGNMENTBATCH
# SENDER_MAPPING = OrderedDict(
#     COMPANYNAME="contact_id",
#     STREETADDRESS1="shipper_street",
#     STREETADDRESS2="shipper_street2",
#     STREETADDRESS3="",
#     CITY="shipper_city",
#     PROVINCE="",
#     POSTCODE="shipper_zip",
#     COUNTRY="shipper_country",
#     ACCOUNT="",
#     VAT="",
#     CONTACTNAME="shipper_name",
#     CONTACTDIALCODE="",
#     CONTACTTELEPHONE="",
#     CONTACTEMAIL="",
# )

COLLECTION_MAPPING = OrderedDict(
    # COLLECTIONADDRESS=None,
    SHIPDATE="",
    # PREFCOLLECTTIME=None,
    # ALTCOLLECTTIME=None,
    COLLINSTRUCTIONS=""
)

RECEIVER_MAPPING = OrderedDict(
    COMPANYNAME="consignee_name",
    STREETADDRESS1="street",
    STREETADDRESS2="street2",
    # STREETADDRESS3="street3",
    CITY="city",
    # PROVINCE="",
    POSTCODE="zip",
    COUNTRY="country_code",
    # VAT="",
    CONTACTNAME="contact",
    # CONTACTDIALCODE="",
    # CONTACTTELEPHOPNE="consignee_mobile",
    # CONTACTEMAIL="consignee_email",
)

DELIVERY_MAPPING = OrderedDict(
    COMPANYNAME="consignee_name",
    STREETADDRESS1="street",
    STREETADDRESS2="street2",
    # STREETADDRESS3="street3",
    CITY="city",
    # PROVINCE="",
    POSTCODE="zip",
    # COUNTRY="",
    # VAT="",
    # CONTACTNAME="",
    # CONTACTDIALCODE="",
    # CONTACTTELEPHOPNE="consignee_mobile",
    # CONTACTEMAIL="consignee_email",
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
    # RECEIVER=OrderedDict(),
    # DELIVERY=OrderedDict(),
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
    PACKAGE=OrderedDict(),
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


def tnt_decode_initial_response(data):
    access_code = None
    if "COMPLETE" in data:
        access_code = data.split(":")[1]
    return access_code


class TNTLabel(AbstractLabel):

    def __init__(self, test_platform=False):
    # def __init__(self, sender, consignment, code, test_platform=False):

        # self.check_model(sender, SENDER_MODEL, 'company')
        # ADDRESS_MODEL["country_code"] = {
        #     'in': GLS_countries_prefix(), 'required': True}
        # SENDER_MODEL["shipper_country"] = {
        #     'in': GLS_countries_prefix(), 'required': True}
        # if test_platform:
        #     url = URL_TEST  # Replace this with the authentication details instead of using a url.
        # else:
        #     url = URL_PROD
        url = URL_PROD
        # url_separ = url.find('.com/') + 4  # Update for notation on TNT URL
        # start = 0
        # if url[:8] == 'https://':  # Update if TNT uses https
        #     start = 8
        # self.webservice_location = url[start:url_separ]
        self.webservice_location = url
        # self.webservice_method = url[url_separ:]
        self.webservice_method = url
        self.filename = LABEL_FILE_NAME
        # self.sender = sender

    # def add_specific_keys(self, address):
    #     res = {}
    #     res['T090'] = 'NOSAVE'
    #     res['T750'] = ''
    #     res['T200'] = ''
    #     res['T8977'] = ''   # RefDest
    #     if address['country_code'] == 'FR':
    #         res['T082'] = 'UNIQUENO'
    #     return res

    def get_barcode_uniship(self, all_dict, address):
        # get datas for uniship barcode
        if address['country_norme3166']:
            items = [
                'A',  # barcode version
                all_dict['T8915'],
                all_dict['T8914'],
                self.uniship_product,
                address['country_norme3166'],
                all_dict['T330'],    # postal code
                all_dict['T8905'],   # total parcel number
                all_dict['T8702'],   # total parcel number datamatrix
                all_dict['T8973'],   # sequence
                '',                  # ref expe
                all_dict['T860'],    # consignee name
                all_dict['T861'],    # supplément raison sociale1
                all_dict['T862'],    # supplément raison sociale2
                all_dict['T863'],    # street
                '',                  # N° de rue
                all_dict['T864'],    # city
                all_dict['T871'],    # tel
                '',                  # ref customer
                all_dict['T8975'],
                all_dict['T530'],    # weight
            ]
            code = '|'.join(items) + '|'
            # code needs to be fixed size
            code += (304 - len(code)) * ' '
            return {'T8917': code}
        else:
            # TODO : is not raised correctly to ERP
            raise Exception(
                "There is no key 'country_norme3166' in the " +
                "given dictionnary 'address' for the country '%s' : " +
                "this data is required" % address['country_code'])

    def select_label(self, parcel, all_dict, address, failed_webservice=False):
        self.filename = '_' + parcel
        if address['country_code'] == 'UK' and not failed_webservice:
            zpl_file = 'label.mako'
        else:
            if failed_webservice:
                self.filename += '_rescue'
            zpl_file = 'label_uniship.mako'
        template_path = os.path.join(os.path.dirname(__file__), zpl_file)
        with open(template_path, 'r') as template:
            content = template.read()
            # all_dict.update(self.get_barcode_uniship(all_dict, address))
        return content

#     def get_result_analysis(self, result, all_dict):
#         component = result.split(':')
#         code, message = component[0], component[1]
#         if code == 'E000':
#             return True
#         else:
#             logger.info("""Web service access problem :
# code: %s ; message: %s ; result: %s""" % (code, message, result))
#             if message == 'T330':
#                 zip_code = ''
#                 if all_dict['T330']:
#                     zip_code = all_dict['T330']
#                 raise Exception(
#                     "Postal code '%s' is wrong (relative to the "
#                     "destination country)" % zip_code)
#             elif message == 'T100':
#                 cnty_code = ''
#                 if all_dict['T100']:
#                     cnty_code = all_dict['T100']
#                 raise Exception("Country code '%s' is wrong" % cnty_code)
#             else:
#                 if code == 'E999':
#                     logger.info(
#                         "Unibox server (web service) is not responding")
#                 else:
#                     logger.info("""
#         >>> An unknown problem is happened : check network connection,
#         webservice accessibility, sent datas and so on""")
#                 logger.info("""
#         >>> Rescue label will be printed instead of the standard label""")
#             return False
    def get_xsl(self):
        req_url = "https://express.tnt.com/expresswebservices-website/stylesheets/HTMLAddressLabelRenderer.xsl"
        xsl_response = requests.get(req_url)
        xsl_response_text = xsl_response.text.encode('utf-8')
        return et.XML(xsl_response_text)

    def get_label(self, request_data):
        """
        :param request_data: <str> Response from tnt request
        :return: <boolean> Success or Fail, <binary> file to be attached
        """
        success, initial_response = self.get_webservice_response(request_data)
        if not success:
            return False, initial_response

        # Validate response returned by initial request
        # access_code = '926734877'
        access_code = tnt_decode_initial_response(initial_response)
        success, access_code_response = self.get_webservice_response("GET_LABEL:%s" % access_code)
        if not success:
            return False, access_code_response
        access_code_response = access_code_response.encode("utf-8")

        xml = et.XML(access_code_response)
        xslt = self.get_xsl()
        transform = et.XSLT(xslt)
        dom = transform(xml)
        dom_as_pdf = pdfkit.from_string(
            et.tostring(self.cleanup_html(dom)),
            False,
            # css=css_files,
        )
        label_as_ascii = binascii.b2a_base64(dom_as_pdf)
        return True, label_as_ascii


    # def get_label(self, authentication, collection, preftime, alttime, address, pack):
    # def get_label(self, request_data):
        tracking_number = False
        # self.check_model(authentication, AUTHENTICATION_MODEL, 'authentication')
        # self.check_model(parcel, PARCEL_MODEL, 'package')
        # self.check_model(address, ADDRESS_MODEL, 'partner')
        # self.product_code, self.uniship_product = self.get_product(
        #     address['COUNTRY'])
        # self.check_model(delivery, DELIVERY_MODEL, 'delivery')
        # delivery['tnt_origin_reference'] = self.set_origin_reference(  # Change when TNT shipping methods are set
        #     parcel, address)
        # transform human keys in GLS keys (with 'T' prefix)
        # T_authentication = self.map_semantic_keys(AUTHENTICATION_MAPPING, authentication)
        # T_sender = self.map_semantic_keys(SENDER_MAPPING, self.sender)
        # T_collection = self.map_semantic_keys(COLLECTION_ADDRESS_MAPPING, self.sender)
        # T_preftime = self.map_semantic_keys(PREFCOLLECTTIME_MAPPING, preftime)
        # T_alttime = self.map_semantic_keys(ALTCOLLECTTIME_MAPPING, alttime)
        # T_details = self.map_semantic_keys(DETAILS_MAPPING, details)
        # T_receiver = self.map_semantic_keys(RECEIVER_MAPPING, address)
        # T_delivery = self.map_semantic_keys(DELIVERY_MAPPING, address)
        # merge all datas

        # failed_webservice = False

        # refactor webservice response failed and webservice downed
        # if isinstance(response, dict):
        #     if self.get_result_analysis(response['RESULT'], all_dict):
        #         all_dict.update(response)
        #         tracking_number = all_dict['T8913']
        #     else:
        #         failed_webservice = True
        #         label_content = self.select_label(
        #             parcel['parcel_number_label'],
        #             all_dict, address,
        #         )
        # else:
        #     failed_webservice = True
        # label_content = self.select_label(
        #     parcel['parcel_number_label'], all_dict, address,
        #     failed_webservice=failed_webservice)
        # # some keys are not defined by GLS but are in mako template
        # # this add empty values to these keys
        # keys_without_value = self.validate_mako(label_content, all_dict.keys())
        # if keys_without_value:
        #     empty_mapped = (zip(keys_without_value,
        #                         [''] * len(keys_without_value)))
        #     all_dict.update(dict(empty_mapped))
        # try:
        #     tpl = Template(label_content).render(**all_dict)
        #     content2print = tpl.encode(
        #         encoding=REPORT_CODING, errors=ERROR_BEHAVIOR)
        #     return {
        #         "content": content2print,
        #         "tracking_number": tracking_number,
        #         'filename': self.filename,
        #         'request': request,
        #         'raw_response': raw_response,
        #     }
        # except:
        #     traceback = RichTraceback()
        #     for (filename, lineno, function, line) in traceback.traceback:
        #         logger.info("File %s, line %s, in %s"
        #                     % (filename, lineno, function))
        #     raise InvalidDataForMako(
        #         "%s: %s"
        #         % (str(traceback.error.__class__.__name__), traceback.error))

    # Because the XSL doesn't work properly we have to parse for certain elements in the rendered html
    # to make adjustments to the following elements
    def cleanup_html(self, dom):
        # Fix barcode image
        for barcode_elem in dom.xpath("//td[@height='150']/img"):
            new_barcode = "<img src='https://express.tnt.com/barbecue/?data={barcode_number}&amp;type=UCC128&amp;appid=6&amp;height=105'/>".format(
                barcode_number=barcode_elem.getparent().text)
            barcode_elem.addnext(et.XML(new_barcode))
            barcode_elem.getparent().remove(barcode_elem)
        # Fix 1x1 pixel
        for pixel_elem in dom.xpath("//img[@width='1']"):
            pixel_elem.getparent().remove(pixel_elem)
        # Fix page break
        for pagebreak_elem in dom.xpath("//script")[:1]:
            new_pagebreak = "<div style='page-break-before: always;'></div>"
            pagebreak_elem.addnext(et.XML(new_pagebreak))
            pagebreak_elem.getparent().remove(pagebreak_elem)
        # Fix a-circumflex on number of labels
        for td_elem in dom.xpath("//td"):
            if td_elem.text and "\xc3\x82\xc2\xa0" in td_elem.text.encode("utf-8"):
                td_elem.text = td_elem.text.encode("utf-8").replace("\xc3\x82\xc2\xa0", "").decode("utf-8")
        # Fix a-circumflex on telephone number
        for td_elem in dom.xpath("//td[@class='tntTelephone']"):
            td_elem.addnext(
                et.XML("<td nowrap='nowrap' class='tntTelephone' align='center'>Telephone <br/> 01827 303030</td>"))
            td_elem.getparent().remove(td_elem)
        return dom

    def get_webservice_response(self, request):

        request = "xml_in=" + request
        res = requests.post(self.webservice_location, data=request, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        if res.status_code != 200:
            _logger.info("TNT Response: {0} || {1}".format(res.status_code, res.text))
            return False, res

        datas = res.text
        return True, datas

    def validate_mako(self, template, available_keys):
        import re
        keys2match = []
        for match in re.findall(r'\$\{(.+?)\}+', template):
            keys2match.append(match)
        unmatch = list(set(keys2match) - set(available_keys))
        not_in_mako_but_known_case = ['T8900', 'T8901', 'T8717', 'T8911']
        unknown_unmatch = list(unmatch)
        for elm in not_in_mako_but_known_case:
            if elm in unknown_unmatch:
                unknown_unmatch.remove(elm)
        if len(unknown_unmatch) > 0:
            logger.info("GLS carrier : these keys \n%s\nare defined "
                        "in mako template but without valid replacement "
                        "values\n" % unknown_unmatch)
        return unmatch
