# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'Email Compose',
    'category': 'Productivity/Discuss',
    'license': 'LGPL-3',
    'description': 'Allow to send an simple email with Mail Compose.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'application': True,
    'installable': True,
    'depends': [
        'mail',
    ],
    'data': [
        # Data
        'data/mail_templates_email_layouts.xml',

        # Views
        'wizard/mail_compose_message.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pyper_mail_email_compose/static/src/core/**/*',
        ],
    },
}
