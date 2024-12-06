# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Drawer Workspace',
    'category': 'Tools',
    'license': 'Other proprietary',
    'description': 'Move company menu in drawer.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'depends': [
        'base',
        'web',
        'pyper_drawer',
        'pyper_menu',
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('after', 'pyper_drawer/static/src/**/*.variables.scss', 'pyper_drawer_workspace/static/src/**/*.variables.scss'),
        ],
        'web.assets_backend': [
            'pyper_drawer_workspace/static/src/webclient/**/*',
        ],
    }
}
