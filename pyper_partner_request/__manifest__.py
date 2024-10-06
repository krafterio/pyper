# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Partner Requests',
    'category': 'Tools',
    'license': 'Other proprietary',
    'description': 'Register and manage requests for support or assistance.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'images': ['static/description/icon.png'],
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'application': True,
    'installable': True,
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'security/res_groups.xml',
        'security/res_partner_request_security.xml',
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/res_partner_request_views.xml',
        'views/menu.xml',
    ],
}
