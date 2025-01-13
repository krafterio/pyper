# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Purchase Manager',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Override of default purchase addon.',
    'summary': 'Override default purchase templates.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'purchase',
    ],
    'data': [
        # Views
        'views/purchase_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pyper_purchase_manager/static/src/scss/style.scss',
        ],
    }
}
