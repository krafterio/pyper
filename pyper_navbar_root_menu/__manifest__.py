# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'Navbar Root Menu',
    'category': 'Hidden/Tools',
    'license': 'LGPL-3',
    'description': 'Extend Web Interface with Root Menu in main navbar.',
    'version': '1.1',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'depends': [
        'base',
        'web',
        'pyper',
        'pyper_menu',
    ],
    'assets': {
        'web._assets_primary_variables': [
            'pyper_navbar_root_menu/static/src/**/*.variables.scss',
        ],
        'web.assets_backend': [
            'pyper_navbar_root_menu/static/src/webclient/**/*',
        ],
    },
}
