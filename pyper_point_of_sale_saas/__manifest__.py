# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Point Of Sale SaaS',
    'category': 'Hidden',
    'license': 'Other proprietary',
    'description': 'Point Of Sale configuration for SaaS',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'auto_install': [
        'point_of_sale',
        'pyper_saas',
    ],
    'depends': [
        'point_of_sale',
        'pyper_saas',
    ],
    'data': [
        # Data
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pyper_point_of_sale_saas/static/src/app/*',
        ]
    }
}
