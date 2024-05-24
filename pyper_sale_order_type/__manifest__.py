# Copyright Krafter SAS <hey@krafter.io>
# Odoo Proprietary License (see LICENSE file).

{
    'name': 'Pyper Sale Order Type',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Addon dedicated to add sale order types',
    'version': '17.0.0.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'application': True,
    'depends': [
        'sale',
    ],
    'data': [
        # Views
        'views/sale_order_views.xml',
    ],
}
