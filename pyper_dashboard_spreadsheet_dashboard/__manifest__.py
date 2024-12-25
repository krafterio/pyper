# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Dashboard Spreadsheet Integration',
    'category': 'Productivity',
    'license': 'Other proprietary',
    'description': 'Make compatible Spreadsheet Dashboard with Pyper Dashboard',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'application': True,
    'post_init_hook': 'post_init_hook',
    'auto_install': [
        'pyper_dashboard',
        'spreadsheet_dashboard',
    ],
    'depends': [
        'base',
        'web',
        'pyper_dashboard',
        'pyper_setup',
        'spreadsheet_dashboard',
    ],
    'data': [
        # Views
        'views/res_config_settings_views.xml',
        'views/res_groups_views.xml',
    ],
}
