# Copyright Krafter SAS <hey@krafter.io>
# Odoo Proprietary License (see LICENSE file).

{
    'name': 'Pyper sale Manager',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Override of default sale addon.',
    'version': '17.0.0.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'sale',
    ],
    'data': [
        # Views
        'views/sale_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pyper_sale_manager/static/src/scss/style.scss',
        ],
    }
}
