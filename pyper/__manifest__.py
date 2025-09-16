# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'Pyper',
    'category': 'Hidden/Tools',
    'license': 'LGPL-3',
    'description': 'Base of Pyper addons.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'base',
        'base_setup',
        'web',
    ],
    'data': [
        # Data
        'data/ir_cron_data.xml',

        # Views
        'views/webclient_templates.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('before', 'web/static/src/**/*.variables.scss', 'pyper/static/src/**/*.variables.scss'),
        ],
        'web.assets_backend': [
            'pyper/static/src/core/dropdown/**/*',
            'pyper/static/src/core/ui/**/*',
            'pyper/static/src/views/fields/**/*',
            'pyper/static/src/views/form/**/*',
            'pyper/static/src/webclient/menus/**/*',
            'pyper/static/src/webclient/window/**/*',
        ],
    },
}
