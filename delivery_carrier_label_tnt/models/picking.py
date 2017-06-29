# coding: utf-8
# © 2015 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime, date, timedelta
import base64
import logging
from collections import OrderedDict

import binascii
from lxml import etree as et

from openerp import models, api, fields, _, exceptions
from openerp.exceptions import Warning as UserError
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from ..report.label import TNTLabel, InvalidDataForMako
from ..report.exception_helper import (InvalidAccountNumber)
from ..report.label_helper import (
    InvalidValueNotInList,
    InvalidMissingField,
    InvalidType,)

# logging.basicConfig(format='%(asctime)-15s %(clientip)s %(user)-8s %(message)s', level=logging.INFO)
_logger = logging.getLogger(__name__)

try:
    import pycountry
except (ImportError, IOError) as err:
    _logger.debug(err)


def raise_exception(message):
    raise UserError(map_except_message(message))


def map_except_message(message):
    """ Allows to map vocabulary from external library
        to Odoo vocabulary in Exception message
    """
    model_mapping = {
        'shipper_country': 'partner_id.country_id.code',
        # 'customer_id': 'UK or International field '
        #                '(settings > config > carrier > TNT)',
    }
    for key, val in model_mapping.items():
        message = message.replace(key, val)
    return message


class StockPicking(models.Model):
    _inherit = "stock.picking"

    carrier_tracking_ref = fields.Char(copy=False)

    @api.multi
    def do_transfer(self):
        """ Used by wizard stock_tranfert_details and js interface """
        res = super(StockPicking, self).do_transfer()
        for picking in self:
            if picking.carrier_type == 'tnt':
                picking.label_subtask()
        return res

    @api.multi
    def action_done(self):
        """ Used by stock_picking_wave """
        res = super(StockPicking, self).action_done()
        for picking in self:
            if picking.carrier_type == 'tnt':
                picking.label_subtask()
        return res

    @api.multi
    def label_subtask(self):
        self.ensure_one()
        self.set_pack_weight()
        if self.company_id.tnt_generate_label:
            self.generate_labels()

    @api.multi
    def _customize_tnt_picking(self):
        "Use this method to override tnt picking"
        self.ensure_one()
        return True

    @api.model
    def _prepare_authentication_tnt(self):
        creds = OrderedDict()
        if self.company_id.tnt_test:
            creds.update({"COMPANY": self.company_id.tnt_test_user_id})
            creds.update({"PASSWORD": self.company_id.tnt_test_user_password})
        else:
            creds.update({"COMPANY": self.company_id.tnt_user_id})
            creds.update({"PASSWORD": self.company_id.tnt_user_password})
        creds.update({"APPID": "IN"})
        creds.update({"APPVERSION": "2.2"})
        return creds

    @api.model
    def _prepare_global_tnt(self):
        res = {}
        param_m = self.env['ir.config_parameter']
        tnt_keys = ['carrier_tnt_warehouse', 'carrier_tnt_customer_code']  # AMS has multiple warehouses
        configs = param_m.search([('key', 'in', tnt_keys)])
        for elm in configs:
            res[elm.key] = elm.value
        return res

    # Return preferred collection time as a dict to use for mapping
    @api.model
    def _prepare_preftime(self):
        preftime = OrderedDict()
        preftime.update({"FROM": "10:00"})
        preftime.update({"TO": "11:00"})
        return preftime

    # Return preferred collection time as a dict to use for mapping
    @api.model
    def _prepare_alttime(self):
        alttime = OrderedDict()
        alttime.update({"FROM": "12:00"})
        alttime.update({"TO": "13:00"})
        return alttime

    @api.model
    def _prepare_address_name_tnt(self, partner):
        consignee = partner.name
        contact = partner.name
        if partner.parent_id and partner.use_parent_address:
            consignee = partner.parent_id.name
        return {'consignee_name': consignee, 'contact': contact}

    # Return delivery/receiver address as dict for value mapping
    @api.multi
    def _prepare_address_tnt(self):
        self.ensure_one()
        address = OrderedDict()
        res = self.env['res.partner']._get_split_address(
            self.partner_id, 3, 35)  # 3 Lines, max 35 characters
        # address['street'], address['street2'], address['street3'] = res
        country_code = (self.partner_id and
                        self.partner_id.country_id.code or 'UK')
        iso_3166 = pycountry.countries.get(alpha_2=country_code).numeric
        destination = self._prepare_address_name_tnt(self.partner_id)
        address.update({"COMPANYNAME": destination['consignee_name'][:35]}),
        address.update({"STREETADDRESS1": res[0]}),
        if res[1]:
            address.update({"STREETADDRESS2": res[1]}),
        if res[2]:
            address.update({"STREETADDRESS3": res[2]}),
        address.update({"CITY": self.partner_id.city}),
        address.update({"PROVINCE": False}),
        address.update({"POSTCODE": self.partner_id.zip}),
        address.update({"COUNTRY": self.partner_id.country_id.code or 'GB'}),
        address.update({"VAT": False}),
        address.update({"CONTACTNAME": destination['contact'][:35]}),
        # Choose mobile or phone and split to dialcode and main numbers. Then update address dict
        address.update(self.telephone_split(self.partner_id))
        address.update({"CONTACTEMAIL": self.partner_id.email}),

        return address

    # TODO Split this for package details
    @api.multi
    def _prepare_delivery_tnt(self, number_of_packages):
        self.ensure_one()
        shipping_date = self.min_date or self.date
        shipping_date = datetime.strptime(
            shipping_date, DEFAULT_SERVER_DATETIME_FORMAT)
        delivery = {}
        delivery.update({
            'consignee_ref': self.name[:20],
            'additional_ref_1': u'',
            'additional_ref_2': self.name[:20],
            'shipping_date': shipping_date.strftime('%Y%m%d'),
            'commentary': self.note,
            'parcel_total_number': number_of_packages,
        })
        return delivery

    # Return senders address as dict for value mapping
    @api.multi
    def _prepare_sender_tnt(self):
        self.ensure_one()
        partner = self._get_label_sender_address()
        # global_infos = self._prepare_global_tnt()
        # sender = {'contact_id': self.company_id.name,
        #           # 'customer_id': global_infos['carrier_tnt_customer_code'],
        #           'contact_id_inter': self.company_id.name,
        #           # 'outbound_depot': global_infos['carrier_tnt_warehouse']
        #           }
        # if partner.country_id:
        #     sender['country'] = partner.country_id.name
        # sender.update({
        #     'shipper_street': partner.street,
        #     'shipper_street2': partner.street2,
        #     'shipper_name': partner.name,
        #     'shipper_country': partner.country_id.code,
        #     'shipper_zip': partner.zip,
        #     'shipper_city': partner.city,
        # })
        sender = OrderedDict()
        sender.update({"COMPANYNAME": self.company_id.name})
        sender.update({"STREETADDRESS1": partner.street})
        sender.update({"STREETADDRESS2": partner.street2})
        sender.update({"STREETADDRESS3": partner.street2})
        sender.update({"CITY": partner.city})
        sender.update({"PROVINCE": partner.state_id.name})
        sender.update({"POSTCODE": partner.zip})
        sender.update({"COUNTRY": partner.country_id.code})
        sender.update({"ACCOUNT": self.company_id.tnt_account_number})
        sender.update({"VAT": partner.vat})
        sender.update({"CONTACTNAME": partner.name})
        # Choose mobile or phone and split to dialcode and main numbers. Then update sender dict
        sender.update(self.telephone_split(partner))
        sender.update({"CONTACTEMAIL": partner.email})
        return sender

    def telephone_split(self, partner):
        res = OrderedDict()
        if partner.mobile:
            res.update({"CONTACTDIALCODE": partner.mobile.replace(" ", "")[:4]})
            res.update({"CONTACTTELEPHONE": partner.mobile.replace(" ", "")[4:]})
            return res
        elif partner.phone:
            res.update({"CONTACTDIALCODE": partner.phone.replace(" ", "")[:7]})
            res.update({"CONTACTTELEPHONE": partner.phone.replace(" ", "")[7:]})
            return res
        else:
            res.update({"CONTACTDIALCODE": "Unavailable"})
            res.update({"CONTACTTELEPHONE": "Unavailable"})
            return res

    # TODO Combine with todo above to prepare package details
    @api.model
    def _prepare_pack_tnt(self, package, pack_number):
        package_details = OrderedDict()
        package_details.update({"ITEMS": "1"})
        package_details.update({"DESCRIPTION": "Box #"})
        package_details.update({"LENGTH": "0.2"})
        package_details.update({"HEIGHT": "0.2"})
        package_details.update({"HEIGHT": "0.2"})
        package_details.update({})
        return {
            'parcel_number_label': pack_number,
            'parcel_number_barcode': pack_number,
            'custom_sequence': self._get_sequence('tnt'),
            'weight': "{0:05.2f}".format(package.weight)
        }

    @api.model
    def _prepare_package_details(self):
        return {
            "items": len(self._get_packages_from_picking()),
        }

    @api.multi
    def _generate_tnt_labels(self, service, packages=None):
        """ Generate labels and write tracking numbers received """
        self.ensure_one()
        pack_number = 0
        deliv = {}
        traceability = []
        labels = []
        authentication = self._prepare_authentication_tnt()
        sender = self._prepare_sender_tnt()
        collection = self._prepare_sender_tnt()
        preftime = self._prepare_preftime()
        alttime = self._prepare_alttime()
        conref = self.name
        address = self._prepare_address_tnt()
        package_details = self._get_package_totals(self._get_packages_from_picking())
        base_data = self._prepare_base_request_data(authentication, sender, preftime, alttime, conref, address, package_details)
        if packages is None:
            packages = self._get_packages_from_picking()
        delivery = self._prepare_delivery_tnt(len(packages))
        for package in packages:
            pack_number += 1
            pack = et.fromstring(self._prepare_packages_tnt(package))
            base = et.fromstring(base_data)
            pack_node = base.xpath("//DELIVERYINST")[0]
            pack_node.addnext(pack)
            base_data = et.tostring(base, encoding="UTF-8", method="xml", standalone=False)
        # Remove unneeded newline
        base_data = base_data.replace("\n", "")
        success, label_as_ascii = service.get_label(base_data)
        if not success:
            raise exceptions.Warning("Error code %s received: %s" %(label_as_ascii.status_code, label_as_ascii.reason))
        self.create_tnt_attachment(label_as_ascii)
        # either user self.company_id.tnt_connumber = blah
        # or self.company_id.write({'tnt_connumber': blah})
        if self.company_id.tnt_generate_connumber:
            self.company_id.tnt_connumber = self._get_next_con_number()




        # for package in packages:
        #     pack_number += 1
        #     addr = address.copy()
        #     deliv.clear()
        #     deliv = delivery.copy()
        #     pack = self._prepare_pack_tnt(package, pack_number)
        #
        #     # Change this to only make the request to TNT. Doesn't need to process data)
        #     # label = self.get_zpl(service, deliv, addr, pack, authentication, collection, preftime, alttime)
        #
        #     print "past label!!"
        #     pack_vals = {'parcel_tracking': label['tracking_number'],
        #                  'carrier_id': self.carrier_id.id}
        #     package.write(pack_vals)
        #     _logger.info("package wrote")
        #     label_info = {
        #         'package_id': package.id,
        #         'file': label['content'],
        #         'file_type': 'zpl2',
        #         'type': 'binary',
        #         'name': label['filename'] + '.zpl',
        #     }
        #     if label['tracking_number']:
        #         label_info['name'] = '%s%s.zpl' % (label['tracking_number'],
        #                                            label['filename'])
        #     if self.company_id.country_id.code == 'UK':
        #         labels.append(label_info)
        #     traceability.append(self._record_webservice_exchange(label, pack))
        # self.write({'number_of_packages': pack_number})
        # if self.company_id.tnt_traceability and traceability:
        #     self._save_traceability(traceability, label)
        # self._customize_tnt_picking()

        return labels

    # @api.multi
    # def _save_traceability(self, traceability, label):
    #     self.ensure_one()
    #     separator = '=*' * 40
    #     content = u'\n\n%s\n\n\n' % separator
    #     content = content.join(traceability)
    #     content = (
    #         u'Company: %s\nCompte France: %s \nCompte Etranger: %s \n\n\n') % (
    #         self.company_id.name or '',
    #         self.company_id.gls_fr_contact_id or '',
    #         self.company_id.gls_inter_contact_id or '') + content
    #     data = {
    #         'name': u'GLS_traceability.txt',
    #         'res_id': self.id,
    #         'res_model': self._name,
    #         'datas': base64.b64encode(content.encode('utf8')),
    #         'type': 'binary',
    #         'file_type': 'text/plain',
    #     }
    #     return self.env['shipping.label'].create(data)

    # def _record_webservice_exchange(self, label, pack):
    #     trac_infos = ''
    #     if 'raw_response' in label and 'request' in label:
    #         trac_infos = (
    #             u'Sequence Colis GLS:\n====================\n%s \n\n'
    #             u'Web Service Request:\n====================\n%s \n\n'
    #             u'Web Service Response:\n=====================\n%s \n\n') % (
    #             pack['custom_sequence'],
    #             label['request'],
    #             label['raw_response'])
    #     return trac_infos

    # def get_zpl(self, authentication, service, delivery, address, pack):
    # authentication, sender, collection, preftime, alttime, details, address, delivery
    def get_zpl(self, service, delivery, address, pack, authentication, collection, preftime, alttime):
    # def get_zpl(self, service, authentication, address, collection, preftime, alttime, delivery, pack):
        try:
            # _logger.info(
            #     "TNT label generating for delivery '%s', pack '%s'",
            #     delivery['consignee_ref'], pack['parcel_number_label'])
            result = service.get_label(authentication, collection, preftime, alttime, address, pack)

        except (InvalidMissingField,
                InvalidDataForMako,
                InvalidValueNotInList,
                InvalidAccountNumber,
                InvalidType) as e:
            raise_exception(e.message)
        except Exception, e:
            raise UserError(e.message)
        return result

    # To be updated following TNT methods for webservice being down
    @api.multi
    def generate_shipping_labels(self, package_ids=None):
        """ Add label generation for TNT """
        self.ensure_one()
        if self.carrier_type == 'tnt':
            sender = self._prepare_sender_tnt()
            consignment = self._prepare_packages_tnt
            # gls has a rescue label without webservice required
            # if webservice is down
            # rescue label is also used for international carrier
            test = False
            if self.company_id.tnt_test:
                test = True
            try:
                _logger.info(
                    "Connecting to TNT web service")
                # service = TNTLabel(
                #     sender, consignment, self.carrier_code, test_platform=test)
                service = TNTLabel(test_platform=test)
            except InvalidMissingField as e:
                raise_exception(e.message)
            except Exception as e:
                raise_exception(e.message)
            self._check_existing_shipping_label()
            return self._generate_tnt_labels(
                service, packages=package_ids)
        return (super(StockPicking, self)
                .generate_shipping_labels(package_ids=package_ids))

    @api.model
    def _get_sequence(self, label_name):
        sequence = self.env['ir.sequence'].next_by_code(
            'stock.picking_%s' % label_name)
        if not sequence:
            raise UserError(
                _("There is no sequence defined for the label '%s'")
                % label_name)
        return sequence

    @api.multi
    def get_shipping_cost(self):
        return 0

    def dict_to_xml_data(self, parent, data):
        for key, val in data.items():
            item = et.SubElement(parent, key)
            if not isinstance(val, (dict, bool)):
                item.text = val
            if isinstance(val, (unicode, str, bool)):
                pass
            else:
                self.dict_to_xml_data(item, val)
        return et.tostring(parent, encoding='UTF-8', method='xml', standalone=False)

    def _get_package_volume(self, packages):
        combined_volume = 0
        for package in packages:
            product_id = package.quant_ids.product_id
            if not float(product_id.volume) > 0:
                raise exceptions.Warning("Product: {0} has an invalid volume. Please set and try again".format(product_id.name))
            else:
                combined_volume += product_id.volume
        return combined_volume

    def _get_package_weight(self, packages):

        combined_weight = 0
        for package in packages:
            product_id = package.quant_ids.product_id
            if not float(product_id.weight) > 0:
                raise exceptions.Warning("Product: {0} has an invalid weight. Please set and try again".format(product_id.name))
            else:
                combined_weight += product_id.weight
        if combined_weight > 70:
            raise exceptions.Warning("Package weight cannot exceed 70kg. Please split to smaller packages")
        return combined_weight

    def _get_package_totals(self, packages):
        import pdb;pdb.set_trace()
        package_details = {
            "items": str(len(packages)),
            "goodsvalue": str(sum(package.quant_ids.product_id.sales_price_gbp for package in packages)),
            "totalweight": str(self._get_package_weight(packages)),
            "totalvolume": str(self._get_package_volume(packages)),
            "insurancevalue": str(sum(package.quant_ids.product_id.sales_price_gbp for package in packages)),
        }
        return package_details

    def _prepare_base_request_data(self, authentication, sender, preftime, alttime, conref, address, package_totals):
        base_dict = OrderedDict()
        base_dict.update({"LOGIN": authentication})
        base_dict.update({"CONSIGNMENTBATCH": OrderedDict()})
        base_dict.setdefault("CONSIGNMENTBATCH").update({"SENDER": sender})
        base_dict.setdefault("CONSIGNMENTBATCH").setdefault("SENDER").update({"COLLECTION": OrderedDict()})
        # base_dict.setdefault("CONSIGNMENTBATCH").setdefault("SENDER").setdefault("COLLECTION").update({"COLLECTIONADDRESS": self.sender.copy()})
        base_dict.setdefault("CONSIGNMENTBATCH").setdefault("SENDER").setdefault("COLLECTION").update({"SHIPDATE": datetime.strftime(datetime.today() + timedelta(days=1), "%d/%m/%Y")})
        base_dict.setdefault("CONSIGNMENTBATCH").setdefault("SENDER").setdefault("COLLECTION").update({"PREFCOLLECTTIME": preftime})
        base_dict.setdefault("CONSIGNMENTBATCH").setdefault("SENDER").setdefault("COLLECTION").update({"ALTCOLLECTTIME": alttime})
        base_dict.setdefault("CONSIGNMENTBATCH").setdefault("SENDER").setdefault("COLLECTION").update({"COLLINSTRUCTIONS": False})
        base_dict.setdefault("CONSIGNMENTBATCH").update({"CONSIGNMENT": OrderedDict()})
        base_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").update({"CONREF": conref})
        base_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").update({"DETAILS": OrderedDict()})

        # Check if custom consignment numbers are used and update base_dict if true
        if self.company_id.tnt_generate_connumber:
            base_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"CONNUMBER": self._calculate_checksum(self.company_id.tnt_connumber)})

        base_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"RECEIVER": address})
        # base_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"DELIVERY": address})
        base_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"CUSTOMERREF": False})
        base_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"CONTYPE": "N"})
        base_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"PAYMENTIND": "S"})
        base_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"ITEMS": package_totals.get("items")})
        base_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"TOTALWEIGHT": package_totals.get("totalweight")})
        base_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"TOTALVOLUME": package_totals.get("totalvolume")})
        base_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"CURRENCY": "GBP"})
        base_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"GOODSVALUE": package_totals.get("goodvalue")})
        base_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"INSURANCEVALUE": package_totals.get("insurancevalue")})
        base_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"INSURANCECURRENCY": "GBP"})
        base_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"SERVICE": self.carrier_code})
        # base_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"OPTION": "09N"})
        base_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"DESCRIPTION": False})
        base_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"DELIVERYINST": False})

        if self.product_id.hazardous_id:
            base_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"HAZARDOUS": "Y"})
            base_dict.setdefault("CONSIGNMENTBATCH").setdefault("CONSIGNMENT").setdefault("DETAILS").update({"UNNUMBER": str(self.product_id.hazardous_id.name_id)})

        base_dict.update({"ACTIVITY": OrderedDict()})
        base_dict.setdefault("ACTIVITY").update({"CREATE": OrderedDict()})
        base_dict.setdefault("ACTIVITY").setdefault("CREATE").update({"CONREF": self.name})
        base_dict.setdefault("ACTIVITY").update({"RATE": OrderedDict()})
        base_dict.setdefault("ACTIVITY").setdefault("RATE").update({"CONREF": self.name})
        base_dict.setdefault("ACTIVITY").update({"BOOK": OrderedDict()})
        base_dict.setdefault("ACTIVITY").setdefault("BOOK").update({"CONREF": self.name})
        base_dict.setdefault("ACTIVITY").update({"SHIP": OrderedDict()})
        base_dict.setdefault("ACTIVITY").setdefault("SHIP").update({"CONREF": self.name})
        base_dict.setdefault("ACTIVITY").update({"PRINT": OrderedDict()})
        base_dict.setdefault("ACTIVITY").setdefault("PRINT").update({"CONNOTE": OrderedDict()})
        base_dict.setdefault("ACTIVITY").setdefault("PRINT").setdefault("CONNOTE").update({"CONREF": self.name})
        base_dict.setdefault("ACTIVITY").setdefault("PRINT").update({"LABEL": OrderedDict()})
        base_dict.setdefault("ACTIVITY").setdefault("PRINT").setdefault("LABEL").update({"CONREF": self.name})
        base_dict.setdefault("ACTIVITY").setdefault("PRINT").update({"MANIFEST": OrderedDict()})
        base_dict.setdefault("ACTIVITY").setdefault("PRINT").setdefault("MANIFEST").update({"CONREF": self.name})
        base_dict.setdefault("ACTIVITY").setdefault("PRINT").update({"INVOICE": OrderedDict()})
        base_dict.setdefault("ACTIVITY").setdefault("PRINT").setdefault("INVOICE").update({"CONREF": self.name})
        # base_dict.setdefault("ACTIVITY").setdefault("PRINT").update({"EMAILTO": OrderedDict()})
        # base_dict.setdefault("ACTIVITY").setdefault("PRINT").setdefault("EMAILTO").update({"CONREF": self.name})
        # base_dict.setdefault("ACTIVITY").setdefault("PRINT").update({"EMAILFROM": OrderedDict()})
        # base_dict.setdefault("ACTIVITY").setdefault("PRINT").setdefault("EMAILFROM").update({"CONREF": self.name})
        base_dict.setdefault("ACTIVITY").update({"SHOW_GROUPCODE": False})

        root = et.Element('ESHIPPER')
        return self.dict_to_xml_data(root, base_dict)

    def _prepare_packages_tnt(self, package):

        package_dict = OrderedDict()
        package_dict.update({"ITEMS": "1"})
        package_dict.update({"DESCRIPTION": package.quant_ids.product_id.name})
        package_dict.update({"LENGTH": "1"})
        package_dict.update({"HEIGHT": "1"})
        package_dict.update({"WIDTH": "1"})
        if package.quant_ids.product_id.weight and package.quant_ids.product_id.weight > 0:
            package_dict.update({"WEIGHT": str(package.quant_ids.product_id.weight)})
        else:
            package_dict.update({"WEIGHT": "1"})
        # package_dict.update({"ARTICLE": OrderedDict()})
        # package_dict.setdefault("ARTICLE").update({"ITEMS": ""})
        # package_dict.setdefault("ARTICLE").update({"DESCRIPTION": ""})
        # package_dict.setdefault("ARTICLE").update({"WEIGHT": ""})
        # package_dict.setdefault("ARTICLE").update({"INVOICEVALUE": ""})
        # package_dict.setdefault("ARTICLE").update({"INVOICEDESC": ""})
        # package_dict.setdefault("ARTICLE").update({"HTS": ""})
        # package_dict.setdefault("ARTICLE").update({"COUNTRY": ""})

        root = et.Element('PACKAGE')
        package_xml = self.dict_to_xml_data(root, package_dict)

        return package_xml



    def create_tnt_attachment(self, newdom_as_ascii):
        """
        :param newdom_as_ascii: Binary file pulled from create_tnt_label()
        :return: <id> for ir.attachment model, to be added to self.env.context['attach_id']
        """
        IrAttachment = self.env['ir.attachment']
        attach_data = {
            'name': 'TNT_Packing_List.pdf',
            'datas': binascii.b2a_base64(str(base64.b64decode(newdom_as_ascii))),
            'description': 'Shipping Label',
            'res_name': self.name,
            'res_model': 'stock.picking',
            'res_id': self.id,
            'type': 'binary',
        }
        attachment = IrAttachment.search([('res_id', '=', self.id), ('res_name', '=', self.name)])
        if not attachment:
            attachment = IrAttachment.create(attach_data)
        else:
            attachment.write(attach_data)
        return attachment.id

    def _calculate_checksum(self, con_number):
        digit_weights = [8, 6, 4, 2, 3, 5, 9, 7]
        mod_method = 11
        number_sum = 0

        for idx, digit in enumerate(con_number):
            number_sum += int(digit) * digit_weights[idx]

        remainder = float(number_sum / mod_method)
        check_digit = int(mod_method - remainder)
        if check_digit == 10:
            check_digit = 0
        if check_digit == 11:
            check_digit = 5

        return con_number + str(check_digit)

    def _get_next_con_number(self):
        next_con_number = int(self.company_id.tnt_connumber) + 1
        return str(next_con_number).zfill(8)
