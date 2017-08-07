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

from openerp import models, fields, api, exceptions


class ResCompany(models.Model):

    _inherit = "res.company"

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
    tnt_connumber = fields.Char(
        string="Next Consignment Number",
        default="00000001",
        help="The next custom consignment number to use",

    )
    # tnt_traceability = fields.Boolean(
    #     string='Traceability',
    #     help="Record traceability informations in Delivery Order "
    #          "attachment: web service request and response")
    tnt_generate_label = fields.Boolean(
        string='Automatically Generate Label',
        help="Generate label when delivery is done")
    tnt_test = fields.Boolean(
        string='Test Mode',
        help="Use testing webservice")

    @api.constrains('tnt_connumber')
    @api.one
    def _check_tnt_con_number(self):
        if len(self.tnt_connumber) != 8:
            raise exceptions.Warning("Consignment number must be 8 digits")



