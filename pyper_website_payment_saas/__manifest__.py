# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'Website Payment SaaS',
    'category': 'Hidden',
    'license': 'LGPL-3',
    'description': 'Payment provider rules for SaaS',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'auto_install': [
        'pyper_website_saas',
        'payment',
    ],
    'depends': [
        'pyper_website_saas',
        'payment',
    ],
    'data': [
        'data/rules.xml',
    ],
}
