# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'CRM SaaS',
    'category': 'Hidden',
    'license': 'Other proprietary',
    'description': 'CRM configuration for SaaS',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'auto_install': [
        'crm',
        'pyper_saas',
    ],
    'depends': [
        'crm',
        'pyper_saas',
    ],
    'demo': [
        # Data
        'data/mail_template_demo.xml',
    ],
}
