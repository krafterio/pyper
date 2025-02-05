# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Website Banner',
    'category': 'Hidden',
    'license': 'Other proprietary',
    'description': 'Add a banner header on website',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'web',
        'website',
    ],
    'data': [
        'views/website_banner_views.xml',
        'views/website_banner_template.xml',
        'security/ir.model.access.csv',
    ],
}
