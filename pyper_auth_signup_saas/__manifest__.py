# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Auth Signup SaaS',
    'category': 'Hidden',
    'license': 'Other proprietary',
    'description': 'Auth Signup configuration for SaaS',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'auto_install': [
        'auth_signup',
        'pyper_saas',
    ],
    'depends': [
        'auth_signup',
        'pyper_saas',
    ],
    'data': [
        # Data
        'data/mail_template_data.xml',
        'views/auth_signup_templates_email.xml',
    ],
}
