# -*- coding: utf-8 -*-

from openerp import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    dry_ice = fields.Boolean(
        string='Dry Ice',
        help='Does this product need to be packaged and shipped in dry ice'
    )
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
