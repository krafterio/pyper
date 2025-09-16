# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'Dashboard Spreadsheet Integration',
    'category': 'Productivity',
    'license': 'LGPL-3',
    'description': 'Make compatible Spreadsheet Dashboard with Pyper Dashboard',
    'version': '1.1',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
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
        # Data
        'data/res_config_settings.xml',

        # Views
        'views/res_config_settings_views.xml',
        'views/res_groups_views.xml',
    ],
}
