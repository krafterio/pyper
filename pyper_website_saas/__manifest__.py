# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'Website SaaS',
    'category': 'Hidden',
    'license': 'LGPL-3',
    'description': 'Website configuration for SaaS',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'auto_install': [
        'pyper_saas',
        'web',
        'website',
    ],
    'depends': [
        'pyper_saas',
        'web',
        'website',
    ],
    'data': [
        'data/rules.xml',
        'views/website_templates.xml',
    ],
}
