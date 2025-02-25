# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Digest SaaS',
    'category': 'Hidden',
    'license': 'Other proprietary',
    'description': 'Digest configuration for SaaS',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'auto_install': [
        'digest',
        'pyper_saas',
    ],
    'depends': [
        'digest',
        'pyper_saas',
    ],
    'data': [
        # Data
        'data/digest_data.xml',
    ],
}
