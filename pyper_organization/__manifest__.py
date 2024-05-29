# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Pyper Organization',
    'category': 'Hidden',
    'license': 'Other proprietary',
    'description': 'Base to build multi-tenant application',
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
        'pyper_web_theme',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',
        'security/organization_security.xml',

        # Views
        'views/organization_views.xml',
        'views/res_config_settings_views.xml',
        'views/res_users_views.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('before', 'web/static/src/**/*.variables.scss', 'pyper_organization/static/src/**/*.variables.scss'),
        ],

        'web.assets_backend': {
            'pyper_organization/static/src/webclient/**/*',
        },
    },
}
