# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).
{
    'name': 'Global Search',
    'category': 'Hidden/Tools',
    'license': 'LGPL-3',
    'description': 'Add global search for all available models',
    'version': '1.1',
    'author': 'Krafter SAS',
    'website': 'https://krafter.io',
    'maintainer': [
        'Krafter SAS',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': False,
    'depends': [
        'base',
        'web',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Views
        'views/ir_global_search_model_views.xml',

        # Menu
        'views/menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pyper_global_search/static/src/webclient/**/*',
        ],
    },
}
