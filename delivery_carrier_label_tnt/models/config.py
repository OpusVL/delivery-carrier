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

from openerp import models, api, _, fields
from openerp.exceptions import Warning as UserError


class TNTConfigSettings(models.TransientModel):
    _name = 'tnt.config.settings'
    _inherit = 'res.config.settings'
    _description = 'TNT carrier configuration'

    def _default_company(self):
        return self.env.user.company_id

    company_id = fields.Many2one(
        comodel_name='res.company', string='Company',
        required=True, default=_default_company)
    account_number = fields.Char(
        related="company_id.tnt_account_number"
    )
    user_id = fields.Char(
        related="company_id.tnt_user_id"
    )
    user_password = fields.Char(
        related="company_id.tnt_user_password"
    )
    test_id = fields.Char(
        related="company_id.tnt_test_user_id"
    )
    test_password = fields.Char(
        related="company_id.tnt_test_user_password"
    )
    generate_connumber = fields.Boolean(
        related="company_id.tnt_generate_connumber"
    )
    connumber = fields.Char(
        related="company_id.tnt_connumber"
    )
    test = fields.Boolean(
        related="company_id.tnt_test"
    )

    @api.onchange('company_id')
    def onchange_company_id(self):
        # update related fields
        if not self.company_id:
            return
        company = self.company_id
        self.user_id = company.tnt_user_id
        self.user_password = company.tnt_user_password
        self.test_id = company.tnt_test_user_id
        self.test_password = company.tnt_test_user_password
        # self.traceability = company.tnt_traceability
        # self.generate_label = company.tnt_generate_label
        self.test = company.tnt_test
        self.generate_connumber = company.tnt_generate_connumber
