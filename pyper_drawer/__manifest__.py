# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Pyper Drawer',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Extend Web Interface with drawer.',
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
        'web._assets_secondary_variables': [
            ('after', 'web/static/src/scss/secondary_variables.scss', 'pyper_drawer/static/src/**/*.variables.scss'),
        ],
        'web.assets_backend': [
            'pyper_drawer/static/src/webclient/**/*',
        ],
    },
}
