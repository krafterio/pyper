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
    'auto_install': [
        'web',
        'mail',
        'pyper_web_theme',
    ],
    'depends': [
        'base',
        'web',
        'mail',
        'pyper_web_theme',
    ],
    'data': [
        # Views
        'views/mail_message_views.xml',
    ],
    'assets': {
        'web._assets_secondary_variables': [
            'pyper_web_theme_activity/static/src/core/**/*.variables.scss',
        ],
        'web.assets_backend': [
            'pyper_web_theme_activity/static/src/core/**/*',
            'pyper_web_theme_activity/static/src/webclient/**/*',
        ],
    },
}
