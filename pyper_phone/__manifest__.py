# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
{
    'name': 'Phone Extra',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Add additional fields dedicated to phones',
    'version': '1.0',
    'author': 'Krafter SAS',
    'website': 'https://krafter.io',
    'maintainer': [
        'Krafter SAS',
    ],
    'installable': True,
    'application': False,
    'auto_install': [
        'base',
        'web',
        'phone_validation',
    ],
    'depends': [
        'base',
        'web',
        'phone_validation',
    ],
}
