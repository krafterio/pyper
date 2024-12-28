# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'User Email Signature',
    'category': 'Technical',
    'license': 'Other proprietary',
    'description': 'Allow to use multiple email signatures.',
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
        # Security
        'security/ir.model.access.csv',
        'security/ir_rule.xml',

        # Views
        'views/res_users_views.xml',
    ],
}
