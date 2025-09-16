# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

{
    'name': 'Open AI Stream',
    'category': 'Technical',
    'license': 'LGPL-3',
    'description': 'Base to send message to Open AI and receive a stream in live.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'external_dependencies': {
        'python': [
            'openai',
        ]
    },
    'depends': [
        'base',
        'web',
        'pyper_openai_connector',
    ],
    'assets': {
        'web.assets_backend': [
            'pyper_openai_stream/static/src/views/**/*',
        ],
    },
}
