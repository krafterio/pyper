# Copyright Krafter SAS <hey@krafter.io>
# Odoo Proprietary License (see LICENSE file).

{
    'name': 'Queue Job for UI Kit',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Queue Job for Full UI Kit of Pyper',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'auto_install': [
        'pyper_ui_kit',
        'pyper_queue_job',
    ],
    'depends': [
        'base',
        'pyper_ui_kit',
        'pyper_queue_job',
        'pyper_queue_job_bus',
    ],
    'assets': {
        'web.assets_backend': [
            'pyper_ui_kit_queue_job/static/src/core/**/*',
        ],
    }
}
