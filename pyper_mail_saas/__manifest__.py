# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Mail SaaS',
    'category': 'Hidden',
    'license': 'Other proprietary',
    'description': 'Mail configuration for SaaS',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'depends': [
        'base',
        'web',
        'mail',
    ],
    'data': [
        # Data
        'data/mail_tempates_email_layouts.xml',
    ],
}
