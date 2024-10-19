# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
{
    'name': 'Web View Menu',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Add saved views in menus',
    'version': '1.0',
    'author': 'Krafter SAS',
    'website': 'https://krafter.io',
    'maintainer': [
        'Krafter SAS',
    ],
    'installable': True,
    'application': False,
    'auto_install': [
        'pyper_web_view',
        'pyper_menu_icon',
    ],
    'depends': [
        'base',
        'bus',
        'web',
        'pyper_web_view',
        'pyper_menu_icon',
    ],
    'data': [
        # Security
        'security/ir_ui_menu_security.xml',

        # Views
        'views/ir_views_views.xml',
    ],
    'assets': {
        'web.assets_backend': {
            'pyper_web_view_menu/static/src/webclient/**/*',
        },
    },
}
