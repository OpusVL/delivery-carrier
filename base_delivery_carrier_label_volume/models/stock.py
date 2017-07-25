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

        self.volume = self.length * self.width * self.height


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    consignment_volume = fields.Float(string="Consignment Volume", compute='_compute_consignment_volume')

    def _compute_consignment_volume(self):

        total_volume = 0.00
        for picking in self:

            for operation in picking.pack_operation_ids:
                for result_package_id in operation.result_package_id:
                    if result_package_id.length and result_package_id.width and result_package_id.height:
                        total_volume = result_package_id.length * result_package_id.width * result_package_id.height

        self.volume = total_volume
