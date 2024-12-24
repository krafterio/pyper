# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Email Sync',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Sync all messages from IMAP account',
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
        # Security
        'security/ir_attachment_security.xml',

        # Views
        'views/fetchmail_server_views.xml',
    ],
}
