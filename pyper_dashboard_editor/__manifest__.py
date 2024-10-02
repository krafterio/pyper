# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Dashboard Editor',
    'category': 'Productivity',
    'license': 'Other proprietary',
    'description': 'Build custom dashboards in drag and drop',
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
        'pyper_dashboard',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Views
        'views/dashboard_board_views.xml',
        'views/dashboard_dashboard_views.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            'pyper_dashboard_editor/static/src/**/*.variables.scss',
        ],

        'web.assets_backend': [
            'pyper_dashboard_editor/static/src/webclient/**/*',
        ],
    },
}
