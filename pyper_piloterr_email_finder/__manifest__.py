# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Piloterr email finder',
    'category': 'Sales/CRM',
    'license': 'Other proprietary',
    'description': 'Added the ability to retrieve a contact\'s e-email address from piloterr',
    'summary': 'Added the ability to retrieve a contact\'s e-email address from piloterr',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'application': True,
    'installable': True,
    'depends': [
        'pyper_piloterr_connector',
    ],
    'data': [
        # Views
        'views/res_partner_views.xml',
    ],
}
