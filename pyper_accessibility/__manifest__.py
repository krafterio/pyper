# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Pyper Accessibility',
    'category': 'Extra Tools',
    'license': 'Other proprietary',
    'summary': 'Customize user interface for better inclusivity',
    'description': 'Customize user interface for better inclusivity.',
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
        # Views
        'views/assets.xml',
        'views/res_users_views.xml',
    ],
    'assets': {
        'pyper_accessibility.assets': [
            ('include', 'pyper_accessibility.assets_backend.variables'),
            ('include', 'pyper_accessibility.assets_backend'),
        ],

        'pyper_accessibility.assets_backend.variables': [
            '/pyper_accessibility/static/src/**/*.variables.scss',
        ],

        'pyper_accessibility.assets_backend': [
            '/pyper_accessibility/static/src/**/*.scss',
        ],
    }
}
