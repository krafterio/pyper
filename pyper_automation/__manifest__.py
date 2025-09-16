# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'Automation',
    'category': 'Hidden/Tools',
    'license': 'LGPL-3',
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
        'views/base_automation_views.xml',
        'views/ir_action_server_views.xml',
    ],
}
