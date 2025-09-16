# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'Sale Extra',
    'category': 'Sales/Sales',
    'license': 'LGPL-3',
    'description': 'Extend Sale features.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'depends': [
        'base_setup',
        'web',
        'sale',
        'sale_management',
    ],
    'data': [
        # Views
        'views/res_config_settings_views.xml',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',

        # Reports
        'report/sale_order_report_template.xml',
        'report/sale_order_management_report_template.xml'
    ],
}
