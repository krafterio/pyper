# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Pyper Automation',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Extend features of Base Automation.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'base_automation',
        'sms',
        'phone_validation',
    ],
    'data': [
        # Views
        'views/ir_action_server_views.xml',
    ],
}
