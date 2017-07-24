# coding: utf-8
# © 2015 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Base Delivery Carrier Package Volume',
    'version': '8.0.0.1.0',
    'author': "Akretion,Odoo Community Association (OCA)",
    'maintener': 'Akretion',
    'category': 'Warehouse',
    'summary': "Adds volume field to packages",
    'depends': [
        'base_delivery_carrier_label',
        'base_delivery_carrier_hazardous',
        'partner_helper',
        'stock_packaging_usability',  # Might not be needed
        'document',
    ],
    'website': 'http://www.akretion.com/',
    'data': [
        'views/stock_view.xml',
    ],
    'demo': [
    ],
    'external_dependencies': {
    },
    'license': 'AGPL-3',
    'tests': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
