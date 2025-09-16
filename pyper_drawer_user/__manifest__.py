# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'Drawer User',
    'category': 'Tools',
    'license': 'LGPL-3',
    'description': 'Move user menu in drawer.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'depends': [
        'base',
        'web',
        'pyper_drawer',
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('after', 'pyper_drawer/static/src/**/*.variables.scss', 'pyper_drawer_user/static/src/**/*.variables.scss'),
        ],
        'web.assets_backend': [
            'pyper_drawer_user/static/src/webclient/**/*',
        ],
    }
}
