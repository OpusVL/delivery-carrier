# -*- coding: utf-8 -*-

from openerp import models, fields


# Add hazardous product to product template, related to hazardous.codes model
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    hazardous_id = fields.Many2one(
        comodel_name='hazardous.codes',
        string='Description',
        help='UN Description of the hazardous material'
    )


class HazardousCodes(models.Model):

    _name = 'hazardous.codes'

    name_id = fields.Integer(
        string="UN Code Number"
    )
    name = fields.Char(
        string="UN Code Description"
    )
