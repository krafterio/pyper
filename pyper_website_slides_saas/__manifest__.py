# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Website Slide SaaS',
    'category': 'Hidden',
    'license': 'Other proprietary',
    'description': 'Website Slide configuration for SaaS',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'auto_install': [
        'website_slides',
        'pyper_saas',
    ],
    'depends': [
        'website_slides',
        'pyper_saas',
    ],
    'data': [
        # Data
        'data/mail_template.xml',
    ],
}
