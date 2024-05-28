# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
{
    'name': 'Pyper Web Theme Activity',
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
        'pyper_activity',
        'pyper_web_theme',
    ],
    'data': [
        'views/mail_message_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pyper_web_theme_activity/static/src/core/**/*',
            'pyper_web_theme_activity/static/src/mail/**/*',
            'pyper_web_theme_activity/static/src/webclient/**/*',
        ],
    },
}
