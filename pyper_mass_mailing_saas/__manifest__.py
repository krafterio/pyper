# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Mass Mailing SaaS',
    'category': 'Hidden',
    'license': 'Other proprietary',
    'description': 'Mass Mailing configuration for SaaS',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'auto_install': [
        'mass_mailing',
        'pyper_saas',
    ],
    'depends': [
        'mass_mailing',
        'pyper_saas',
    ],
    'demo': [
        # Data
        'data/mailing_mailing.xml',
    ],
}
