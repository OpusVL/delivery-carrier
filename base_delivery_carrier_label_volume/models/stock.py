# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import ValidationError


class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    length = fields.Float(string="Length of package (m)", help="Maximum length allowed is 3.6m")
    width = fields.Float(string="Width of package (m)", help="Maximum width allowed is 1.8m")
    height = fields.Float(string="Height of package (m)", help="Maximum height allowed is 2.1m")
    volume = fields.Float(string="Volume of package", compute='_compute_volume')

    @api.depends('length', 'width', 'height')
    def _compute_volume(self):

        self.volume = self.length * self.width * self.height

    @api.constrains('length')
    def _validate_length(self):

        if not self.length > 0:
            raise ValidationError("Please set the package length")

        if self.length > 3.6:
            raise ValidationError("Package length exceeds maximum allowed")

    @api.constrains('width')
    def _validate_width(self):

        if not self.width > 0:
            raise ValidationError("Please set the package width")

        if self.width > 1.8:
            raise ValidationError("Package width exceeds maximum allowed")

    @api.constrains('height')
    def _validate_height(self):

        if not self.height > 0:
            raise ValidationError("Please set the package height")

        if self.height > 2.1:
            raise ValidationError("Package height exceeds maximum allowed")

    # @api.constrains('weight')
    # def _validate_weight(self):
    #     if not self.weight > 0:
    #         raise ValidationError("Please set the package weight")
    #
    #     if self.weight > 70:
    #         raise ValidationError("Package weight exceeds maximum allowed")


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    consignment_volume = fields.Float(string="Consignment Volume", compute='_compute_consignment_volume')

    @api.one
    def _compute_consignment_volume(self):
        total_volume = 0.00
        for picking in self:

            for operation in picking.pack_operation_ids:
                for result_package_id in operation.result_package_id:
                    if result_package_id.length and result_package_id.width and result_package_id.height:
                        total_volume = result_package_id.length * result_package_id.width * result_package_id.height

        self.volume = total_volume
