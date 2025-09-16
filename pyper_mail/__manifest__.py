# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).
{
    'name': 'Mail Extra',
    'category': 'Hidden/Tools',
    'license': 'LGPL-3',
    'description': 'Add extra information',
    'version': '1.0',
    'author': 'Krafter SAS',
    'website': 'https://krafter.io',
    'maintainer': [
        'Krafter SAS',
    ],
    'installable': True,
    'depends': [
        'base',
        'web',
        'mail',
    ],
    'assets': {
        'web.assets_backend': [
            'pyper_mail/static/src/core/**/*',
        ],
    },
    'data': [
        'views/mail_message_views.xml',
    ]
}
