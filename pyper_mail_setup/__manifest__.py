# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
{
    'name': 'Mail Setup',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Base to setup Pyper mail addons',
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
        'pyper_setup',
    ],
    'data': [
        # Views
        'views/res_config_settings_views.xml',
    ],
}
