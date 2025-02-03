# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Custom OAuth Provider',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Custom OAuth Provider',
    'version': '1.0',
    'author': 'Krafter SAS',
    'mainteiner': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'depends': ['base', 'pyper_setup'],
    'data': [
        'views/menu.xml',
        'views/oauth_template.xml',
        'security/ir.model.access.csv',
    ],
}