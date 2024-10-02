# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Navbar Root Menu',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Extend Web Interface with Root Menu in main navbar.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'depends': [
        'base',
        'web',
        'pyper',
        'pyper_menu_icon',
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
