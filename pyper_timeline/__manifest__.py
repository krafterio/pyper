# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Pyper Timeline',
    'category': 'Tools',
    'license': 'Other proprietary',
    'description': 'Timeline component to create views with timeline chart',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'web',
        'pyper_setup',
    ],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            'pyper_timeline/static/src/**/*.variables.scss',
        ],

        'web.assets_backend': {
            'pyper_timeline/static/src/views/**/*',
        },
    },
}
