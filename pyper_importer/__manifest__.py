# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Pyper Importer',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Base to create and manage import from external service.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'base',
        'base_setup',
        'web',
        'pyper_queue_job',
    ],
    'data': [
        'security/ir.model.access.csv',

        'data/action_server_data.xml',

        'views/pyper_importer_endpoint_views.xml',
        'views/pyper_importer_provider_views.xml',
        'views/pyper_queue_job_log_views.xml',
        'views/pyper_queue_job_views.xml',
        'views/res_config_settings_views.xml',

        'wizard/pyper_importer_schedule_wizard_views.xml',
    ],
}
