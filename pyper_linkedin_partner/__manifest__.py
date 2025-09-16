# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'LinkedIn Partner',
    'category': 'Sales/CRM',
    'license': 'LGPL-3',
    'description': 'Add fields dedicated to LinkedIn in partners',
    'summary': 'Add fields dedicated to LinkedIn in partners',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'base',
    ],
    'data': [
        # Views
        'views/res_partner_views.xml',
    ],
}
