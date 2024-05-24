# Copyright Krafter SAS <hey@krafter.io>
# Odoo Proprietary License (see LICENSE file).

{
    'name': 'Pyper contact',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Addon dedicated to contact management',
    'version': '17.0.0.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'application': True,
    'depends': [
        'contacts',
    ],
    'data': [
        # Views
        'views/res_partner_views.xml',
        'views/menu.xml',
    ],
}
