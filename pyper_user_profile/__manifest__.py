# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Pyper user profile',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Pyper addons dedicated to handling user profile and rights.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        # Data
        # Security
        'security/res_groups.xml',
        'security/res_users_role.xml',
        'security/res_users_profile.xml',
        'security/ir.model.access.csv',
        # Views
        'views/res_users_role_views.xml',
        'views/res_users_profile_views.xml',
        'views/res_users_views.xml',
    ],
    'assets': {
    },
}
