# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).
{
    'name': 'Mail Audit Log',
    'category': 'Hidden/Tools',
    'license': 'LGPL-3',
    'description': 'Hide tracking values in mail chatter',
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
        'pyper_mail',
    ],
    'assets': {
        'web.assets_backend': [
            'pyper_mail_audit_log/static/src/core/**/*',
        ],
    },
}
