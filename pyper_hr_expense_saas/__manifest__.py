# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'HR Expense SaaS',
    'category': 'Hidden',
    'license': 'Other proprietary',
    'description': 'HR Expense configuration for SaaS',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'auto_install': [
        'hr_expense',
        'pyper_saas',
    ],
    'depends': [
        'hr_expense',
        'pyper_saas',
    ],
    'data': [
        # Data
        'data/mail_templates.xml',
    ],
}
