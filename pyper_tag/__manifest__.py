# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Smart Tag',
    'category': 'Tools',
    'license': 'Other proprietary',
    'description': 'A generic tag model, built to fit with any odoo model',
    'summary': 'A generic tag model',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
       'web',
    ],
    'data': [
        # Data
        'data/groups.xml',
        
        # Security
        'security/ir.model.access.csv',
        'security/rules.xml',

        # Views
        'views/smart_tag_family_views.xml',
        'views/smart_tag_views.xml',
    ],
}
