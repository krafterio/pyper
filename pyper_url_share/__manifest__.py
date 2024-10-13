# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'URL Share Button',
    'version': '1.0',
    'license': 'Other proprietary',
    'summary': 'Copy URL to clipboard from the systray',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'category': 'Hidden/Tools',
    'depends': [
        'base',
        'web'
    ],
    'assets': {
        'web.assets_backend': [
            'pyper_url_share/static/src/**/*',
        ],
    },
}
