# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Pyper Dashboard',
    'category': 'Productivity',
    'license': 'Other proprietary',
    'description': 'Build custom dashboards',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'application': True,
    'installable': True,
    'depends': [
        'base',
        'web',
    ],
    'data': [
        # Security
        'security/res_groups.xml',
        'security/ir_rule.xml',
        'security/ir.model.access.csv',

        # Views
        'views/dashboard_dashboard_views.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            'pyper_dashboard/static/src/**/*.variables.scss',
        ],

        'web.assets_backend': [
            'pyper_dashboard/static/src/views/**/*',
            'pyper_dashboard/static/src/webclient/**/*',
        ],
    },
}
