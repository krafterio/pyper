# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
{
    'name': 'Web Theme Activity',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Add activity theme for Pyper Web Theme',
    'version': '1.0',
    'author': 'Krafter SAS',
    'website': 'https://krafter.io',
    'maintainer': [
        'Krafter SAS',
    ],
    'installable': True,
    'application': False,
    'depends': [
        'base',
        'mail',
        'pyper_web_theme',
    ],
    'data': [
        # Data
        'data/groups.xml',

        # Views
        'views/mail_message_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'web._assets_secondary_variables': [
            'pyper_web_theme_activity/static/src/core/**/*.variables.scss',
        ],
        'web.assets_backend': [
            'pyper_web_theme_activity/static/src/core/**/*',
            'pyper_web_theme_activity/static/src/mail/**/*',
            'pyper_web_theme_activity/static/src/webclient/**/*',
        ],
    },
}
