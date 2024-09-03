# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Pyper Stack Tracker',
    'category': 'Sales/CRM',
    'license': 'Other proprietary',
    'description': 'Add ability to track partner technical stack',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'application': True,
    'installable': True,
    'depends': [
        'base_automation',
        'pyper_saas',
        'pyper_menu_icon',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Views
        'views/partner_views.xml',
        'views/technology_views.xml',
        'views/technology_type_views.xml',
        'views/code_language_views.xml',
        'views/menu.xml',
    ],
}
