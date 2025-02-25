# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Website Sale Autocomplete SaaS',
    'category': 'Hidden',
    'license': 'Other proprietary',
    'description': 'Website Sale Autocomplete for SaaS',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'auto_install': [
        'website_sale_autocomplete',
        'pyper_saas',
    ],
    'depends': [
        'website_sale_autocomplete',
        'pyper_saas',
    ],
    'data': [
        # Data
        'data/autocomplete.xml',
    ],
}
