# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Pyper Website Snippets',
    'category': 'Hidden',
    'license': 'Other proprietary',
    'description': 'Extend website snippets',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'website',
    ],
    'data': [
        'views/s_top_banner_overflow_image_right_and_left.xml',
        'views/snippets.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/pyper_website_snippets/static/src/scss/style.scss',
        ],
    }
}
