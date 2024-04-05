# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Pyper Sale Extra',
    'category': 'Sales/Sales',
    'license': 'Other proprietary',
    'description': 'Extend Sale features.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'depends': [
        'web',
        'sale',
        'sale_management',
    ],
    'data': [
        'views/sale_order_views.xml',

        'report/sale_order_report_template.xml',
    ],
}
