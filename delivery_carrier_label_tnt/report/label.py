# -*- coding: utf-8 -*-

# #########################################################################
#
# Delivery Carrier Label TNT
# Copyright (C) 2017 OpusVL (<http://opusvl.com/>)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# ########################################################################

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

    print "InvalidMissingField"


def tnt_decode_initial_response(data):
    access_code = None
    if "COMPLETE" in data:
        access_code = data.split(":")[1]
    return access_code


class TNTLabel(AbstractLabel):

    def __init__(self, test_platform=False):

        self.webservice_location = URL_PROD
        # self.webservice_method = url[url_separ:]
        self.webservice_method = URL_PROD
        self.filename = LABEL_FILE_NAME

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
        import pdb;pdb.set_trace()
        request = "xml_in=" + request
        res = requests.post(self.webservice_location, data=request, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        if res.status_code != 200:
            _logger.info("TNT Response: {0} || {1}".format(res.status_code, res.text))
            return False, res

        datas = res.text
        return True, datas
