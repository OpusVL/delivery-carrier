# -*- coding: utf-8 -*-

from openerp import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    dry_ice = fields.Boolean(
        string='Dry ice',
        help='Does this product need to be packaged and shipped in dry ice'
    )
    hazardous = fields.Boolean(
        string='Hazardous',
        help='Does this product contain hazardous materials'
    )
