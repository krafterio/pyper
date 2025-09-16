# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).
{
    'name': 'Web Theme Overlay Menu',
    'category': 'Hidden/Tools',
    'license': 'LGPL-3',
    'description': 'Make compatible Overlay Menu with Pyper Web Theme',
    'version': '1.0',
    'author': 'Krafter SAS',
    'website': 'https://krafter.io',
    'maintainer': [
        'Krafter SAS',
    ],
    'auto_install': [
        'pyper_overlay_menu',
        'pyper_web_theme',
    ],
    'depends': [
        'base',
        'base_setup',
        'web',
        'pyper_overlay_menu',
        'pyper_web_theme',
    ],
    'assets': {
        'web.assets_backend': [
            'pyper_web_theme_overlay_menu/static/src/webclient/**/*',
        ],
    },
}
