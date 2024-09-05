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
        # Top Blocks
        'views/snippets/top_blocks/s_top_app_banner.xml',
        'views/snippets/top_blocks/snippets.xml',

        # Modern Blocks
        'views/snippets/modern_blocks/snippets.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/pyper_website_snippets/static/src/scss/style.scss',
        ],
    }
}
