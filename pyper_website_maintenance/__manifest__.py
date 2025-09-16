# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'Website Maintenance',
    'category': 'Hidden',
    'license': 'LGPL-3',
    'description': 'Maintenance mode for all frontend features like website, portal and eCommerce',
    'version': '1.1',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'website',
    ],
    'data': [
        # Views
        'views/res_config_settings_views.xml',
        'views/website_views.xml',
    ],
}
