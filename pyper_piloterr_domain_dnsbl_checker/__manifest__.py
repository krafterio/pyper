# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Piloterr domain dnsbl checker',
    'category': 'Sales/CRM',
    'license': 'Other proprietary',
    'description': 'Added the ability to know if a contact\'s domain has been configured for anti-spam from piloterr',
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
    ],
}
