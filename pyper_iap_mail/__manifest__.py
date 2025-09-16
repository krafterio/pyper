# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'IAP Mail',
    'category': 'Hidden/Tools',
    'license': 'LGPL-3',
    'description': 'Send email warning when IAP provider threshold is reached.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'auto_install': [
        'iap',
        'mail',
        'pyper_iap',
    ],
    'depends': [
        'iap',
        'mail',
        'pyper_iap',
    ],
    'data': [
        # Views
        'views/iap_account_views.xml',
    ],
}
