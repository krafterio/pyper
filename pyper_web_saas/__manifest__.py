# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'Web SaaS',
    'category': 'Hidden',
    'license': 'LGPL-3',
    'description': 'Web configuration for SaaS',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'auto_install': [
        'pyper_saas',
        'web',
    ],
    'depends': [
        'pyper_saas',
        'base',
        'web',
    ],
    'data': [
        # Data
        'views/webclient_templates.xml',
    ],
}
