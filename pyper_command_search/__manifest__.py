# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'Command Search',
    'category': 'Hidden/Tools',
    'license': 'LGPL-3',
    'description': 'Global search action.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'depends': [
        'base',
        'web',
    ],
    'assets': {
        'web.assets_backend': [
            'pyper_command_search/static/src/core/web/**/*',
        ],
    },
}
