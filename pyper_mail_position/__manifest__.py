# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).
{
    'name': 'Mail Position',
    'category': 'Hidden/Tools',
    'license': 'LGPL-3',
    'description': 'Define the position of chatter',
    'version': '1.1',
    'author': 'Krafter SAS',
    'website': 'https://krafter.io',
    'maintainer': [
        'Krafter SAS',
    ],
    'installable': True,
    'post_init_hook': 'post_init_hook',
    'depends': [
        'base',
        'web',
        'mail',
        'pyper_mail_setup',
    ],
    'data': [
        # Views
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pyper_mail_position/static/src/views/**/*',
        ],
    },
}
