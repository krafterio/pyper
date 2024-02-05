# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
{
    'name': 'Pyper Web Theme',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Add pyper web theme with clean back office theme',
    'version': '1.0',
    'author': 'Krafter SAS',
    'installable': True,
    'application': False,
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'depends': [
        'web',
        'base',
        'base_automation',
        'base_setup',
        'mail',
        'pyper',
        'pyper_drawer',
        'pyper_fonts_phosphor',
        'pyper_command_search',
        'pyper_control_panel',
        'pyper_overlay_menu',
        'pyper_activity',
    ],
    'data': [
        'views/res_config_settings_views.xml',
        'views/mail_message_views.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('before', 'pyper/static/src/**/*.variables.scss', 'pyper_web_theme/static/src/**/*.variables.scss'),
            ('before', 'pyper/static/src/scss/primary_variables.scss', 'pyper_web_theme/static/src/scss/primary_variables.scss'),
        ],
        'web._assets_secondary_variables': [
            ('before', 'pyper/static/src/scss/secondary_variables.scss', 'pyper_web_theme/static/src/scss/secondary_variables.scss'),
        ],
        'web._assets_frontend_helpers': [
            ('prepend', 'pyper_web_theme/static/src/scss/bootstrap_overridden.scss'),
        ],
        'web._assets_backend_helpers': [
            ('before', 'pyper/static/src/scss/bootstrap_overridden.scss', 'pyper_web_theme/static/src/scss/bootstrap_overridden.scss'),
        ],
        'web.assets_frontend': [
            'pyper_web_theme/static/src/scss/style.scss',
        ],
        'web.assets_backend': [
            ('prepend', 'pyper_fonts_phosphor/static/src/scss/phosphor-regular.scss'),
            ('prepend', 'pyper_fonts_phosphor/static/src/scss/phosphor-light.scss'),
            ('prepend', 'pyper_fonts_phosphor/static/src/scss/phosphor-fill.scss'),
            ('before', 'mail/static/src/scss/variables/derived_variables.scss','pyper_web_theme/static/src/mail/derived_variables.scss'),
            ('after', 'web/static/src/search/search_bar/search_bar.xml', 'pyper_web_theme/static/src/search/search_bar/search_bar.xml'),
            ('after', 'mail/static/src/**/web/**/*', 'pyper_web_theme/static/src/utilities/**/*'),
            'pyper_web_theme/static/lib/odoo_ui_icons/*.css',
            'pyper_web_theme/static/src/scss/style.scss',
            'pyper_web_theme/static/src/legacy/**/*',
            'pyper_web_theme/static/src/core/**/*',
            'pyper_web_theme/static/src/views/**/*',
            'pyper_web_theme/static/src/webclient/**/*',
        ],
    },
}
