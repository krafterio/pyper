# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Pyper Overlay Menu',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Extend Web Interface with Overlay Menu.',
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
    'data': [
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('after', 'pyper/static/src/**/*.variables.scss', 'pyper_overlay_menu/static/src/**/*.variables.scss'),
        ],
        'web.assets_backend': [
            'pyper_overlay_menu/static/src/webclient/**/*',
        ],
    },
}
