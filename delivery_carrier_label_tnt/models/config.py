# coding: utf-8
# © 2015 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

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
    test = fields.Boolean(
        related="company_id.tnt_test"
    )
    show_hazardous = fields.Boolean(
        string="Show Hazardous on Products",
        help="Show fields for Dry Ice and Hazardous on products"
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

    # @api.model
    # def default_get(self, fields):
    #     res = super(TNTConfigSettings, self).default_get(fields)
    #     param_m = self.env['ir.config_parameter']
    #     # for field in ['customer_code', 'warehouse']:
    #     for field in ['customer_code']:
    #         if field in fields:
    #             configs = param_m.search(
    #                 [('key', '=', 'carrier_tnt_%s' % field)])
    #             if not configs:
    #                 raise UserError(
    #                     _("'%s' key is missing in 'System Parameter':\n"
    #                       "Add it and set the corresponding value.") % field)
    #             res[field] = configs[0].value
    #     return res
