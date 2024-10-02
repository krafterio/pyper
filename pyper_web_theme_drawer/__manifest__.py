# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
{
    'name': 'Web Theme Drawer',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Make compatible Drawer with Pyper Web Theme',
    'version': '1.0',
    'author': 'Krafter SAS',
    'website': 'https://krafter.io',
    'maintainer': [
        'Krafter SAS',
    ],
    'post_init_hook': 'post_init_hook',
    'auto_install': [
        'pyper_drawer',
        'pyper_web_theme',
    ],
    'depends': [
        'base',
        'base_setup',
        'web',
        'pyper_drawer',
        'pyper_web_theme',
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('before', 'pyper_drawer/static/src/**/*.variables.scss', 'pyper_web_theme_drawer/static/src/webclient/drawer/**/*.variables.scss'),
        ],

        'web.assets_backend': [
            'pyper_web_theme_drawer/static/src/webclient/**/*',
        ],
    },
}
