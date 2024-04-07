# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Pyper Account Extra',
    'category': 'Accounting/Payment',
    'license': 'Other proprietary',
    'description': 'Extend Account features.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'depends': [
        'web',
        'account',
    ],
    'data': [
        # Views
        'views/res_config_settings_views.xml',

        # Reports
        'report/invoice_report_template.xml',
    ],
}
