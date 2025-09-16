# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'Security Role',
    'category': 'Technical',
    'license': 'LGPL-3',
    'description': 'Allow to add security role included security groups on user.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'depends': [
        'base',
        'base_setup',
        'web',
    ],
    'data': [
        # Data
        'data/ir_action_server.xml',

        # Security
        'security/res_groups.xml',

        # Views
        'views/res_config_settings_views.xml',
        'views/res_groups_views.xml',
        'views/res_users_views.xml',
    ],
}
