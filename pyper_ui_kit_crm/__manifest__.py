# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'CRM for UI Kit',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'CRM for Full UI Kit of Pyper',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'auto_install': [
        'pyper_ui_kit',
        'crm',
    ],
    'depends': [
        'base',
        'pyper_ui_kit',
        'crm',
    ],
    'assets': {
        'web.assets_backend': [
            'pyper_ui_kit_crm/static/src/views/**/*',
        ],
    }
}
