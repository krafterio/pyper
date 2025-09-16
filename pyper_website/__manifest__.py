# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'Website',
    'category': 'Hidden',
    'license': 'LGPL-3',
    'description': 'Extend website features',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'auto_install': [
        'web',
        'website',
    ],
    'depends': [
        'web',
        'website',
    ],
    'data': [
        'views/website_pages_views.xml',
    ],
}
