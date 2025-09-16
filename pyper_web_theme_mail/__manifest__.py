# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).
{
    'name': 'Web Theme Mail',
    'category': 'Hidden/Tools',
    'license': 'LGPL-3',
    'description': 'Add mail theme for Pyper Web Theme',
    'version': '1.1',
    'author': 'Krafter SAS',
    'website': 'https://krafter.io',
    'maintainer': [
        'Krafter SAS',
    ],
    'installable': True,
    'application': False,
    'auto_install': [
        'mail',
        'pyper_web_theme',
    ],
    'depends': [
        'web',
        'mail',
        'pyper_mail',
        'pyper_web_theme',
    ],
    'assets': {
        'web._assets_secondary_variables': [
            'pyper_web_theme_mail/static/src/**/*.variables.scss',
        ],
        'web.assets_backend': [
            'pyper_web_theme_mail/static/src/core/**/*',
            'pyper_web_theme_mail/static/src/webclient/**/*',
        ],
    },
}
