# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Pyper Drawer Header',
    'category': 'Tools',
    'license': 'Other proprietary',
    'description': 'Allow to display user information in drawer.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'application': True,
    'depends': [
        'base',
        'web',
        'pyper',
        'pyper_drawer',
        'mail',
    ],
    'data': [
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('before', 'web/static/src/**/*.variables.scss', 'pyper_drawer_header/static/src/**/*.variables.scss'),
        ],
        'web.assets_backend': [
            'pyper_drawer_header/static/src/webclient/**/*',
            'pyper_drawer_header/static/src/core/**/*',
        ],
    }
}
