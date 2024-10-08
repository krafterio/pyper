# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Ticketing',
    'category': 'Tools',
    'license': 'Other proprietary',
    'description': 'Ticketing system.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'application': True,
    'installable': True,
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'security/ticket_security.xml',
        'security/ticket_creator_group.xml',
        'security/ticket_validator_group.xml',
        'security/ir.model.access.csv',
        'views/ticket_config_settings_views.xml',
        'views/ticket_views.xml',
        'views/menu.xml',
    ],
}
