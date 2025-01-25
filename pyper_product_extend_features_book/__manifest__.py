# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Product extend features book',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'This addon adds book product management.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'product',
        'pyper_product_catalog',
        'pyper_product_extend_features',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Views
        'views/product_category_views.xml',
        'views/product_template_views.xml',
        'views/product_book_publisher_views.xml',
        'views/menu.xml',
    ],
}
