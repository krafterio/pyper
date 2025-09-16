# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'Dashboard',
    'category': 'Productivity',
    'license': 'LGPL-3',
    'description': 'Build custom dashboards',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'application': False,
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
        'views/dashboard_category_views.xml',
        'views/dashboard_dashboard_views.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            'pyper_dashboard/static/src/**/*.variables.scss',
        ],

        'web.assets_backend': [
            'pyper_dashboard/static/src/views/**/*',
            ('remove', 'pyper_dashboard/static/src/views/graph/**'),
            ('remove', 'pyper_dashboard/static/src/views/pivot/**'),

            'pyper_dashboard/static/src/webclient/**/*',
        ],
        'web.assets_backend_lazy': [
            'pyper_dashboard/static/src/views/graph/**',
            'pyper_dashboard/static/src/views/pivot/**',
        ],
    },
}
