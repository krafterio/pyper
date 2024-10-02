# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Piloterr website technologies',
    'category': 'Sales/CRM',
    'license': 'Other proprietary',
    'description': 'Added the ability to identify the technologies used by a website from piloterr',
    'summary': 'Added the ability to identify the technologies used by a website from piloterr',
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
        'pyper_stack_tracker',
        'pyper_partner_scraper',
        'pyper_queue_job',
    ],
    'data': [
        # Views
        'views/res_partner_views.xml',
    ],
}
