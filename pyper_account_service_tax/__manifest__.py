# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'Account Service Tax',
    'category': 'Accounting/Accounting',
    'license': 'LGPL-3',
    'description': 'Add default service taxes.',
    'version': '1.1',
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
