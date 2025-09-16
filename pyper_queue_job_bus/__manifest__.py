# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'Queue Job Bus',
    'category': 'Hidden/Tools',
    'license': 'LGPL-3',
    'description': 'Add notification on queue jobs.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'auto_install': [
        'bus',
        'pyper_queue_job',
    ],
    'depends': [
        'bus',
        'pyper_queue_job',
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('before', 'web/static/src/**/*.variables.scss', 'pyper_queue_job_bus/static/src/**/*.variables.scss'),
        ],

        'web.assets_backend': [
            'pyper_queue_job_bus/static/src/core/**/*',
            'pyper_queue_job_bus/static/src/webclient/**/*',
        ],
    },
}
