# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
{
    'name': 'Mail Audit Log',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
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
    ],
    'assets': {
        'web.assets_backend': [
            'pyper_mail_audit_log/static/src/core/**/*',
        ],
    },
}
