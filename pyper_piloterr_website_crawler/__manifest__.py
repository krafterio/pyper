# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Piloterr website crawler',
    'category': 'Sales/CRM',
    'license': 'Other proprietary',
    'description': 'Add ability to get the HMTL of a web page from piloterr',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'pyper_piloterr_connector',
    ],
    'data': [
        # Views
        'views/res_partner_views.xml',

        # Security
        'security/ir.model.access.csv',
    ],
}
