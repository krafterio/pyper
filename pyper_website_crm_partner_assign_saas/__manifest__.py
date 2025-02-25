# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Website CRM Partner Assign SaaS',
    'category': 'Hidden',
    'license': 'Other proprietary',
    'description': 'Website CRM Partner Assign configuration for SaaS',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'auto_install': [
        'website_crm_partner_assign',
        'pyper_saas',
    ],
    'depends': [
        'website_crm_partner_assign',
        'pyper_saas',
    ],
    'data': [
        # Data
        'data/mail_template_data.xml',
    ],
}
