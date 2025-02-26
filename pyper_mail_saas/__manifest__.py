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
    'auto_install': [
        'web',
        'mail',
        'pyper_saas',
    ],
    'depends': [
        'base',
        'web',
        'mail',
        'pyper_setup',
        'pyper_saas',
    ],
    'data': [
        # Data
        'data/mail_tempates_email_layouts.xml',
        'views/res_config_settings.xml',
    ],
}
