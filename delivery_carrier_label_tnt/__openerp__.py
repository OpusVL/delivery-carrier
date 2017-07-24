# coding: utf-8
# © 2015 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Delivery Carrier Label TNT',
    'version': '8.0.0.1.0',
    'author': "Akretion,Odoo Community Association (OCA)",
    'maintener': 'Akretion',
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
    'website': 'http://www.akretion.com/',
    'data': [
        'data/delivery_carrier.xml',
        'data/sequence.xml',
        'views/config_view.xml',
        'views/stock_view.xml',
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
