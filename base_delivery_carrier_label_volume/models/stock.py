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


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    consignment_volume = fields.Float(string="Consigment Volume", compute='_compute_consignment_volume')

    @api.multi
    def _compute_consignment_volume(self):
        res = dict()
        for picking in self:
            total_volume = 0.00

            for operation in picking.pack_operation_ids:
                for result_package_id in operation.result_package_id:
                    if result_package_id.volume:
                        total_volume += result_package_id.volume

            res[picking.id] = {
                'volume': total_volume
            }
        return res
