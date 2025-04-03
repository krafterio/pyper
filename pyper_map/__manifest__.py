# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Map',
    'category': 'Tools',
    'license': 'Other proprietary',
    'description': 'Map component to create views with map',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'post_init_hook': 'post_init_hook',
    'depends': [
        'web',
        'pyper_setup',
    ],
    'data': [
        # Views
        'views/res_config_settings_views.xml',
        'views/res_partner_views.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            'pyper_map/static/src/**/*.variables.scss',
        ],

        'web.assets_backend': [
            'pyper_map/static/src/**/*',
        ],
    },
}
