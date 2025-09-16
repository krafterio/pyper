# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'Portal SaaS',
    'category': 'Hidden',
    'license': 'LGPL-3',
    'description': 'Portal configuration for SaaS',
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
        'portal',
    ],
    'depends': [
        'pyper_saas',
        'pyper_web_saas',
        'web',
        'portal',
    ],
    'data': [
        'views/portal_templates.xml',
    ],
}
