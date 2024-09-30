# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Drop Contact connector',
    'category': 'Sales/CRM',
    'license': 'Other proprietary',
    'description': 'Add ability to get contact info from LinkedIn from Drop Contact',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'application': True,
    'installable': True,
    'depends': [
        'pyper_queue_job',
        'pyper_partner_scraper',
    ],
    'post_init_hook': '_create_drop_contact_endpoint_config_param',
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Data
        'data/res_partner_actions.xml',

        # Views
        'views/res_partner_views.xml',
        'views/res_partner_drop_contact_batch_views.xml',
        'views/res_config_settings_views.xml',
    ],
}
