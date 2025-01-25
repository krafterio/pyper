# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Piloterr connector',
    'category': 'Sales/CRM',
    'license': 'Other proprietary',
    'description': 'Add ability to get info from piloterr',
    'summary': 'Add ability to get info from piloterr',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'pyper',
        'pyper_queue_job',
    ],
    'data': [
        # Views
        'views/res_config_settings_views.xml',
    ],
}
