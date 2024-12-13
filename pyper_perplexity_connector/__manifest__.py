# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Perplexity AI Connector',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Add ability to use Perplexity AI API',
    'summary': 'Add ability to use Perplexity AI API',
    'version': '1.0',
    'author': 'Krafter SAS',
    'application': True,
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'depends': [
        'base',
        'web',
    ],
    'data': [
        # Views
        'views/res_config_settings_views.xml',
    ],
}
