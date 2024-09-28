# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Pyper Menu Icon',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Extend Web Interface of menu with icon.',
    'version': '1.0',
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
        'pyper_setup',
    ],
    'data': [
        # Views
        'views/ir_ui_menu_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            'pyper_menu_icon/static/src/**/*.variables.scss',
        ],
        'web.assets_backend': [
            'pyper_menu_icon/static/src/webclient/**/*',
        ],
    },
}
