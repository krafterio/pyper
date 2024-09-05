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
        'views/snippets/top_blocks/s_top_banner_overflow_image_variations.xml',
        'views/snippets/top_blocks/s_top_banner_title_with_foreground_image.xml',
        'views/snippets/top_blocks/s_heading_masonry.xml',
        
        'views/snippets/top_blocks/snippets.xml',

        # Modern Blocks
        'views/snippets/modern_blocks/s_containerized_title_block.xml',
        'views/snippets/modern_blocks/s_row_banner_with_kpis.xml',
        'views/snippets/modern_blocks/s_faq_with_title.xml',
        'views/snippets/modern_blocks/s_customer_review_blocks.xml',
        'views/snippets/modern_blocks/s_title_block_with_cards.xml',
        'views/snippets/modern_blocks/s_customer_references_grid.xml',
        'views/snippets/modern_blocks/s_multi_grid_blocks.xml',
        'views/snippets/modern_blocks/s_multi_grid_blocks_with_carousel.xml',
        'views/snippets/modern_blocks/s_tab_references.xml',
        'views/snippets/modern_blocks/s_feature_grid_with_links.xml',
        'views/snippets/modern_blocks/s_three_column_article.xml',
        'views/snippets/modern_blocks/s_section_with_card_link_items.xml',

        'views/snippets/modern_blocks/snippets.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/pyper_website_snippets/static/src/scss/style.scss',
        ],
    }
}
