# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
{
    'name': 'Web Collection',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Link records in collections',
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
        'web',
        'pyper_menu',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',
        'security/ir_collections_security.xml',
        'security/ir_ui_menu_security.xml',

        # Views
        'views/ir_collections_views.xml',
        'views/ir_model_views.xml',
        'views/menu.xml',

        # Wizard
        'wizard/ir_collections_wizard.xml',

        # Data (views dependencies)
        'data/ir_ui_menu_category_data.xml',
    ],
    'assets': {
        'web.assets_backend': {
            'pyper_web_collection/static/src/views/**/*',
            'pyper_web_collection/static/src/webclient/**/*',
        },
    },
}
