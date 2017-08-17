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

{
    'name': 'Delivery Carrier Label TNT',
    'version': '8.0.0.1.0',
    'author': "OpusVL,Odoo Community Association (OCA)",
    'maintainer': 'OpusVL',
    'category': 'Warehouse',
    'summary': "TNT carrier label printing",
    'depends': [
        'base_delivery_carrier_label',
        'base_delivery_carrier_hazardous',
        'base_delivery_carrier_label_volume',
        'partner_helper',
        'stock_packaging_usability',  # Might not be needed
        'document',
    ],
    'website': 'http://opusvl.com/',
    'data': [
        'data/delivery_carrier.xml',
        'data/sequence.xml',
        'views/config_view.xml',
        'views/stock_view.xml',
        'security/ir.model.access.csv'
    ],
    'demo': [
        'demo/config.yml',
        'demo/company.xml',
        'demo/product.xml',
        'demo/stock.picking.csv',
        'demo/stock.move.csv',
    ],
    'external_dependencies': {
        'python': [
            'pycountry',
            'unidecode',
        ],
    },
    'license': 'AGPL-3',
    'tests': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
