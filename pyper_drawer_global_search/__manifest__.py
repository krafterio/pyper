# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).
{
    'name': 'Drawer Global Search',
    'category': 'Hidden/Tools',
    'license': 'LGPL-3',
    'description': 'Add global search input in drawer',
    'version': '1.0',
    'author': 'Krafter SAS',
    'website': 'https://krafter.io',
    'maintainer': [
        'Krafter SAS',
    ],
    'installable': True,
    'application': False,
    'auto_install': [
        'pyper_drawer',
        'pyper_global_search',
    ],
    'depends': [
        'base',
        'web',
        'pyper_drawer',
        'pyper_global_search',
    ],
    'assets': {
        'web._assets_primary_variables': [
            'pyper_drawer_global_search/static/src/**/*.variables.scss',
        ],

        'web.assets_backend': [
            'pyper_drawer_global_search/static/src/webclient/**/*',
        ],
    },
}
