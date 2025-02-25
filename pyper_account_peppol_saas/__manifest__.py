# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Account Peppol SaaS',
    'category': 'Hidden',
    'license': 'Other proprietary',
    'description': 'Account Peppol configuration for SaaS',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'auto_install': [
        'account_peppol',
        'pyper_saas',
    ],
    'depends': [
        'account_peppol',
        'pyper_saas',
    ],
    'data': [
        # Data
        'data/mail_template_email_layouts.xml',
    ],
}
