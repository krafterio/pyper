# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'User Email Signature',
    'category': 'Technical',
    'license': 'LGPL-3',
    'description': 'Allow to use multiple email signatures.',
    'version': '1.1',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'depends': [
        'base',
        'web',
        'mail',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',
        'security/ir_rule.xml',

        # Views
        'views/res_users_views.xml',

        # Wizard
        'wizard/mail_compose_message_views.xml',
    ],
}
