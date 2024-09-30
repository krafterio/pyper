# Copyright Krafter SAS <hey@krafter.io>
# Odoo Proprietary License (see LICENSE file).

{
    'name': 'Pyper partner scraper',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Add blocks that will allow you to scrape partners.',
    'version': '17.0.0.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'base',
    ],
    'data': [
        # Views
        'views/res_partner_views.xml',
    ],
}
