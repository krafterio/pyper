# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'Overlay Menu',
    'category': 'Hidden/Tools',
    'license': 'LGPL-3',
    'description': 'Extend Web Interface with Overlay Menu.',
    'version': '1.1',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'post_init_hook': 'post_init_hook',
    'depends': [
        'base',
        'web',
        'pyper',
        'pyper_menu',
        'pyper_setup',
    ],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('before', 'web/static/src/**/*.variables.scss', 'pyper_overlay_menu/static/src/**/*.variables.scss'),
        ],
        'web.assets_backend': [
            'pyper_overlay_menu/static/src/webclient/**/*',
        ],
    },
}
