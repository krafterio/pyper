# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'IAP',
    'category': 'Hidden/Tools',
    'license': 'LGPL-3',
    'description': 'Base to add custom IAP providers.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'auto_install': [
        'iap',
    ],
    'depends': [
        'iap',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Views
        'views/iap_account_views.xml',
        'wizard/iap_account_update_balance_wizard.xml',
    ],
}
