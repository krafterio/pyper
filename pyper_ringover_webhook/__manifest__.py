# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
{
    'name': 'Ringover Webhook',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Logs phone calls from Ringover',
    'version': '1.0',
    'author': 'Krafter SAS',
    'website': 'https://krafter.io',
    'maintainer': [
        'Krafter SAS',
    ],
    'installable': True,
    'application': False,
    'depends': [
        'base',
        'web',
        'mail',
        'base_automation',
        'pyper_phone',
    ],
    'data': [
        'data/base_automation_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pyper_ringover_webhook/static/src/core/**/*',
        ],
    },
}
