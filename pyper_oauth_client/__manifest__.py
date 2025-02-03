# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Oauth Client',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Management of oauth clients.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'depends': [
        'base',
        'auth_oauth',
        'helpdesk',
        'web',
        'kascade',
        'auth_signup',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Data
        'data/res_users.xml',

        # Views
        'views/auth_oauth_views.xml',
        'views/webclient_templates.xml',
        'views/res_config_settings_views.xml',
        'views/res_users_view.xml'
        
    ]
}
