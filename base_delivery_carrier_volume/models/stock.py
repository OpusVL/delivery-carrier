# -*- coding: utf-8 -*-
from openerp import models, fields, api


class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    length = fields.Float(string="Length of package (m)")
    width = fields.Float(string="Width of package (m)")
    height = fields.Float(string="Height of package (m)")
    volume = fields.Float(string="Volume of package", compute='_compute_volume')

    @api.depends('length', 'width', 'height')
    def _compute_volume(self):

        volume = self.length * self.width * self.height
        return volume
