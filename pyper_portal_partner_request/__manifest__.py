# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Portal Partner Requests',
    'category': 'Tools',
    'license': 'Other proprietary',
    'description': 'Requests system.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'images': ['static/description/icon.png'],
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'application': True,
    'installable': True,
    'depends': [
        'portal',
        'pyper_partner_request',
    ],
    'data': [
        'views/portal_res_partner_request_settings_views.xml',
        'views/portal_res_partner_request_views.xml'
    ],
}
