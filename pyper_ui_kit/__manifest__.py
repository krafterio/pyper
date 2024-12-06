# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
{
    'name': 'UI Kit',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Full UI Kit of Pyper',
    'version': '1.0',
    'author': 'Krafter SAS',
    'website': 'https://krafter.io',
    'maintainer': [
        'Krafter SAS',
    ],
    'application': True,
    'post_init_hook': 'post_init_hook',
    'depends': [
        'base',
        'web',
        'pyper_control_panel',
        'pyper_drawer',
        'pyper_drawer_user',
        'pyper_drawer_workspace',
        'pyper_menu',
        'pyper_url_share',
        'pyper_web_view_menu',
        'pyper_web_theme',
        'pyper_web_theme_icons',
    ],
    'data': [
        # Views
        'views/webclient_templates.xml',
    ],
}
