# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Product condition',
    'category': 'Manufacturing/Repair',
    'license': 'Other proprietary',
    'description': 'This addon adds ability to manage product condition.',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'application': True,
    'post_init_hook': 'activate_variant_on_install',
    'depends': [
        'product',
        'pyper_product_catalog',
        'sale',
        'stock',
    ],
    'data': [
        # Data
        'data/product_condition.xml',
        'data/product_attribute.xml',
        'data/product_attribute_value.xml',

        # Security
        'security/ir.model.access.csv',
        'security/product_security.xml',

        # Views
        'views/product_attribute_views.xml',
        'views/product_template_views.xml',
        'views/product_condition_views.xml',
        'views/conf_setting_views.xml',

        'views/menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pyper_product_condition/static/src/scss/style.scss',
        ]
    },
}
