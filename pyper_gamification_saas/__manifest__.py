# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Gamification SaaS',
    'category': 'Hidden',
    'license': 'Other proprietary',
    'description': 'Gamification configuration for SaaS',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'auto_install': [
        'gamification',
        'pyper_saas',
    ],
    'depends': [
        'gamification',
        'pyper_saas',
    ],
    'data': [
        # Data
        'data/mail_template_data.xml',
    ],
}
