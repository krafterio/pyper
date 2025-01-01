# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
{
    'name': 'Discuss for UI Kit',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Discuss for Full UI Kit of Pyper',
    'version': '1.0',
    'author': 'Krafter SAS',
    'website': 'https://krafter.io',
    'maintainer': [
        'Krafter SAS',
    ],
    'auto_install': [
        'mail',
        'pyper_ui_kit',
    ],
    'depends': [
        'base',
        'web',
        'mail',
        'pyper_ui_kit',
        'pyper_web_theme_mail',
        'pyper_web_theme_discuss',
    ],
    'data': [
        'data/mail_message_install_data.xml',
    ],
}
