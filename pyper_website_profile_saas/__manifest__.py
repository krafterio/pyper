# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Website Profile SaaS',
    'category': 'Hidden',
    'license': 'Other proprietary',
    'description': 'Website Profile configuration for SaaS',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'auto_install': [
        'website_profile',
        'pyper_saas',
    ],
    'depends': [
        'website_profile',
        'pyper_saas',
    ],
    'data': [
        # Data
        'data/mail_template_data.xml',
    ],
}
