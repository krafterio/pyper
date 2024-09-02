# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Pyper effect statusbar',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Pyper addons statusbar effect.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'base',
        'web',
    ],
    'assets': {
        'web.assets_backend': [
            'pyper_effect_statusbar/static/src/views/fields/statusbar/*',
        ],
        'web._assets_core': [
            'pyper_effect_statusbar/static/src/core/**/*',
        ],
        'web.assets_frontend': [
            'web/static/src/core/**/*',
        ],
    },
}
