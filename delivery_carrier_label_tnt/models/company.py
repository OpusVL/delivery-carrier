# coding: utf-8
# © 2015 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ResCompany(models.Model):

    _inherit = "res.company"

    # tnt_uk_contact_id = fields.Char(
    #     string='UK',
    #     size=10,
    #     help='Contact id for TNT UK tranportation (T8914)')
    # tnt_inter_contact_id = fields.Char(
    #     string='International',
    #     size=10,
    #     help='Contact id for TNT International transportation (T8914)')
    tnt_user_id = fields.Char(
        string='Username',
        size=30,
        help='Your TNT ExpressConnect Username'
    )
    tnt_user_password = fields.Char(
        string='Password',
        size=30,
        help='Your TNT ExpressConnect Password'  # Set xml field to 'password="True"'
    )
    tnt_test_user_id = fields.Char(
        string='Test Username',
        size=30,
        help='Your TNT ExpressConnect Test Username'
    )
    tnt_test_user_password = fields.Char(
        string='Test Password',
        size=30,
        help='Your TNT ExpressConnect Test Password'
    )
    tnt_account_number = fields.Char(
        string="Account Number",
        size=10,
        help="Your TNT Account Number"
    )
    tnt_generate_connumber = fields.Boolean(
        string="Custom Consignment Numbers",
        help="Check field to use custom consignment numbers"
    )
    # tnt_traceability = fields.Boolean(
    #     string='Traceability',
    #     help="Record traceability informations in Delivery Order "
    #          "attachment: web service request and response")
    # tnt_generate_label = fields.Boolean(
    #     string='Automatically Generate Label',
    #     help="Generate label when delivery is done")
    tnt_test = fields.Boolean(
        string='Test Mode',
        help="Use testing webservice")
