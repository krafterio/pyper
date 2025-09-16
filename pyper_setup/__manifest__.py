# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'Setup',
    'category': 'Hidden/Tools',
    'license': 'LGPL-3',
    'description': 'Add dedicated app section for Pyper addons in Settings application.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'base',
        'base_setup',
        'web',
    ],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pyper_setup/static/src/webclient/**/*',
        ],
    },
}
