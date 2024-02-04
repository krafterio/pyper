# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Pyper',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Pyper addons superset to build .',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'base_setup',
        'web',
    ],
    'data': [
        'views/webclient_templates.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('after', 'web/static/src/**/*.variables.scss', 'pyper/static/src/**/*.variables.scss'),
        ],
        'web.assets_backend': [
            'pyper/static/src/core/**/*',
            'pyper/static/src/views/**/*',
        ],
    },
}
