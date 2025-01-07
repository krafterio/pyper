# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Piloterr Linkedin lookup',
    'category': 'Sales/CRM',
    'license': 'Other proprietary',
    'description': 'Add ability to get information from LinkedIn',
    'summary': 'Add ability to get information from LinkedIn',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'application': True,
    'installable': True,
    'depends': [
        'pyper_linkedin_partner',
        'pyper_queue_job',
        'pyper_partner_scraper',
    ],
    'data': [
        'views/res_partner_views.xml',
    ],
}
