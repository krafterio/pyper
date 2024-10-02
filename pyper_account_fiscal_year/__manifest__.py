# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Account Fiscal Year',
    'category': 'Accounting/Accounting',
    'license': 'Other proprietary',
    'description': 'Add Fiscal Year for Community Edition.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'depends': [
        'account',
        'web',
    ],
    'data': [
        'data/ir_cron.xml',
        'data/account_fiscal_year_rule.xml',

        'security/ir.model.access.csv',

        'views/account_fiscal_year_views.xml',
        'views/account_invoice_report_views.xml',
        'views/account_move_views.xml',
        'views/account_move_line_views.xml',
    ],
}
