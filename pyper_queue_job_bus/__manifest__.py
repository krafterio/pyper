# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Queue Job Bus',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
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
    'data': [
    ],
}
