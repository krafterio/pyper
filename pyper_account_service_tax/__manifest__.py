# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Account Service Tax',
    'category': 'Accounting/Accounting',
    'license': 'Other proprietary',
    'description': 'Add default service taxes.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'depends': [
        'account',
        'product',
        'web',
    ],
    'data': [
        'views/res_config_settings_views.xml',
    ],
}
