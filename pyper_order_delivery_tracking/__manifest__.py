# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Order delivery tracking',
    'category': 'Tools',
    'license': 'Other proprietary',
    'description': 'Tab on orders to track delivery',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'sale',
        'sale_stock',
    ],
    'data': [
        'views/tracking_tab.xml',
    ],
}
