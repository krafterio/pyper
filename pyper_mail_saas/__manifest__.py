# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'Mail SaaS',
    'category': 'Hidden',
    'license': 'LGPL-3',
    'description': 'Mail configuration for SaaS',
    'version': '1.1',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'auto_install': [
        'web',
        'mail',
        'pyper_saas',
    ],
    'depends': [
        'base',
        'web',
        'mail',
        'pyper_saas',
    ],
    'data': [
        # Data
        'data/mail_tempates_email_layouts.xml',
    ],
}
