# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Piloterr company lookup',
    'category': 'Sales/CRM',
    'license': 'Other proprietary',
    'description': 'Added the ability to retrieve company information from piloterr',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'application': True,
    'installable': True,
    'depends': [
        'piloterr_connector',
        'linkedin_partner',
    ],
    'data': [
        # Views
        'views/res_partner_views.xml',
    ],
}
