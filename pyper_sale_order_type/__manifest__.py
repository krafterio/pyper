# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Sale Order Type',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Addon dedicated to add sale order types',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'sale',
    ],
    'data': [
        # Views
        'views/sale_order_views.xml',
    ],
}
