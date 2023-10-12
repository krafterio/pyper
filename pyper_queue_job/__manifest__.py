# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Pyper Queue Job',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Base to create and manage queue jobs.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'base',
        'web',
    ],
    'data': [
        'security/ir.model.access.csv',

        'data/ir_cron_data.xml',
        'data/action_server_data.xml',

        'views/ir_cron_views.xml',
        'views/pyper_queue_job_views.xml',
        'views/pyper_queue_job_log_views.xml',
    ],
}
