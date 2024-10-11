# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Printing Extended',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Printing Extended.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'data': [
        'views/sale_order_views.xml',
        'report/custom_report.xml',
        'data/report.xml',
    ],
    'depends': [
        'sale',
        'web',
    ],
}