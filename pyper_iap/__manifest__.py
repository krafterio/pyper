# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Pyper IAP',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
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
        # Views
        'views/iap_account_views.xml',
    ],
}
