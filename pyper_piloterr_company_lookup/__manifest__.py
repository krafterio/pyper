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
    'installable': True,
    'depends': [
        'pyper_piloterr_connector',
        'pyper_linkedin_partner',
        'pyper_partner_scraper',
    ],
    'data': [
        # Views
        'views/res_partner_views.xml',
    ],
}
