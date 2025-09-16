# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).
{
    'name': 'Mail Note',
    'category': 'Hidden/Tools',
    'license': 'LGPL-3',
    'description': 'Display the note button in chatter',
    'version': '1.0',
    'author': 'Krafter SAS',
    'website': 'https://krafter.io',
    'maintainer': [
        'Krafter SAS',
    ],
    'installable': True,
    'depends': [
        'base',
        'web',
        'mail',
        'pyper_mail_setup',
    ],
    'data': [
        # Data
        'data/groups.xml',

        # Views
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pyper_mail_note/static/src/core/**/*',
        ],
    },
}
