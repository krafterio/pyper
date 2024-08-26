# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Pyper Security Role',
    'category': 'Technical',
    'license': 'Other proprietary',
    'description': 'Allow to add security role included security groups on user.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'depends': [
        'base',
        'web',
    ],
    'data': [
        # Data
        'data/ir_action_server.xml',

        # Security
        'security/res_groups.xml',

        # Views
        'views/res_groups_views.xml',
        'views/res_users_views.xml',
    ],
}
