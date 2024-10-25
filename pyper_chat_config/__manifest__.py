# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Pyper Chat Config',
    'category': 'Productivity/Discuss',
    'license': 'Other proprietary',
    'description': 'Pyper addon to configure preventing partner to be automatically included in copy of '
    'each mail.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': True,
    'website': 'https://krafter.io',
    'depends': [
        'mail',
    ],
    'data': [
        'views/unsubscribe_partners_wizard_view.xml',
        'views/res_config_settings_views.xml',
        'security/ir.model.access.csv',
    ],
    'assets': {
        'web.assets_backend': [
            'pyper_chat_config/static/src/core/**/*',
        ],
    }
}
