# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Lunch SaaS',
    'category': 'Hidden',
    'license': 'Other proprietary',
    'description': 'Lunch configuration for SaaS',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'auto_install': [
        'lunch',
        'pyper_saas',
    ],
    'depends': [
        'lunch',
        'pyper_saas',
    ],
    'data': [
        # Data
        'data/mail_template_data.xml',
    ],
}
