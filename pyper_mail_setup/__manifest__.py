# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).
{
    'name': 'Mail Setup',
    'category': 'Hidden/Tools',
    'license': 'LGPL-3',
    'description': 'Base to setup Pyper mail addons',
    'version': '1.1',
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
