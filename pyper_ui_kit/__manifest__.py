# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
{
    'name': 'UI Kit',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Full UI Kit of Pyper',
    'version': '1.0',
    'author': 'Krafter SAS',
    'website': 'https://krafter.io',
    'maintainer': [
        'Krafter SAS',
    ],
    'application': True,
    'post_init_hook': 'post_init_hook',
    'depends': [
        'base',
        'web',
        'pyper_control_panel',
        'pyper_drawer',
        'pyper_drawer_user',
        'pyper_menu',
        'pyper_url_share',
        'pyper_web_view_menu',
        'pyper_web_theme',
        'pyper_web_theme_control_panel',
        'pyper_web_theme_icons',
    ],
    'data': [
        # Security
        'security/res_groups.xml',

        # Views
        'views/webclient_templates.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('before', 'pyper_web_theme/static/src/scss/primary_variables.scss', 'pyper_ui_kit/static/src/scss/primary_variables.scss'),
        ],
        'web.assets_backend': [
            ('prepend', 'pyper_ui_kit/static/src/font/archivo.scss'),

            ('prepend', 'pyper_fonts_phosphor/static/src/scss/phosphor-regular.scss'),
            ('prepend', 'pyper_fonts_phosphor/static/src/scss/phosphor-light.scss'),
            ('prepend', 'pyper_fonts_phosphor/static/src/scss/phosphor-fill.scss'),

            'pyper_ui_kit/static/src/**/*.variables.scss',

            'pyper_ui_kit/static/src/scss/pyper_animate.scss',
            'pyper_ui_kit/static/src/scss/style.scss',
            'pyper_ui_kit/static/src/core/**/*',
            'pyper_ui_kit/static/src/mail/**/*',
            'pyper_ui_kit/static/src/search/**/*',
            'pyper_ui_kit/static/src/views/**/*',
            'pyper_ui_kit/static/src/webclient/**/*',

            # Custom CSS
            'pyper_ui_kit/static/src/scss/list.scss',
            'pyper_ui_kit/static/src/scss/form.scss',
            'pyper_ui_kit/static/src/scss/kanban.scss',
            'pyper_ui_kit/static/src/scss/order.scss',

            # Lib
            '/pyper_ui_kit/static/lib/dotlottile-wc/dotlottie-wc.js',
        ],

        'web.assets_frontend': [
            ('prepend', 'pyper_ui_kit/static/src/font/archivo.scss'),
            "pyper_ui_kit/static/src/scss/front/style.scss",
            'pyper_ui_kit/static/src/scss/pyper_animate.scss',
            "pyper_ui_kit/static/src/scss/style.scss",
            "pyper_ui_kit/static/src/scss/front/login.scss",
        ],
    },
}
