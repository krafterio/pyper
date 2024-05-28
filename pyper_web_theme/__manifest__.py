# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
{
    'name': 'Pyper Web Theme',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Add pyper web theme with clean back office theme',
    'version': '1.0',
    'author': 'Krafter SAS',
    'website': 'https://krafter.io',
    'maintainer': [
        'Krafter SAS',
    ],
    'installable': True,
    'application': False,
    'depends': [
        'base',
        'base_setup',
        'web',
        'pyper',
        'pyper_command_search',
        'pyper_control_panel',
        'pyper_fonts_phosphor',
        'pyper_setup',
    ],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            ('before', 'web/static/src/scss/primary_variables.scss', 'pyper_web_theme/static/src/scss/primary_variables.scss'),
            ('before', 'web/static/src/**/*.variables.scss', 'pyper_web_theme/static/src/**/*.variables.scss'),

            # TODO Remove deprecated Pyper assets
            ('remove', 'pyper/static/src/scss/primary_variables.scss'),
            ('remove', 'pyper/static/src/**/*.variables.scss'),
            ('before', 'web/static/src/**/*.variables.scss', 'pyper/static/src/views/fields/**/*.variables.scss'),
        ],
        'web._assets_secondary_variables': [
            ('before', 'web/static/src/scss/secondary_variables.scss', 'pyper_web_theme/static/src/scss/secondary_variables.scss'),

            # TODO Remove deprecated Pyper assets
            ('remove', 'pyper/static/src/scss/secondary_variables.scss'),
        ],
        'web._assets_frontend_helpers': [
            ('prepend', 'pyper_web_theme/static/src/scss/bootstrap_overridden.scss'),
        ],
        'web._assets_backend_helpers': [
            ('before', 'web/static/src/scss/bootstrap_overridden.scss', 'pyper_web_theme/static/src/scss/bootstrap_overridden.scss'),

            # TODO Remove deprecated Pyper assets
            ('remove', 'pyper/static/src/scss/bootstrap_overridden.scss'),
        ],
        'web.assets_frontend': [
            'pyper_web_theme/static/src/scss/style.scss',
        ],
        'web.assets_backend': [
            # TODO Remove deprecated Pyper assets
            ('remove', 'pyper/static/src/legacy/scss/fields.scss'),
            ('remove', 'pyper/static/src/legacy/scss/control_panel_mobile.scss'),
            ('remove', 'pyper/static/src/legacy/scss/dropdown.scss'),
            ('remove', 'pyper/static/src/legacy/scss/touch_device.scss'),
            ('remove', 'pyper/static/src/legacy/scss/modal_mobile.scss'),
            ('remove', 'pyper/static/src/views/kanban/**/*'),
            ('remove', 'pyper/static/src/views/list/**/*'),
            ('remove', 'pyper/static/src/views/pivot/**/*'),
            ('remove', 'pyper/static/src/core/form_renderer/**/*'),
            ('remove', 'pyper/static/src/core/notebook/**/*'),
            ('remove', 'pyper/static/src/core/notifications/**/*'),
            ('remove', 'pyper/static/src/webclient/**/*'),


            ('prepend', 'pyper_fonts_phosphor/static/src/scss/phosphor-regular.scss'),
            ('prepend', 'pyper_fonts_phosphor/static/src/scss/phosphor-light.scss'),
            ('prepend', 'pyper_fonts_phosphor/static/src/scss/phosphor-fill.scss'),
            ('after', 'web/static/src/search/search_bar/search_bar.xml', 'pyper_web_theme/static/src/search/search_bar/search_bar.xml'),
            ('after', 'web/static/src/scss/utilities_custom.scss', 'pyper_web_theme/static/src/utilities/**/*'),
            'pyper_web_theme/static/src/scss/style.scss',
            'pyper_web_theme/static/src/legacy/**/*',
            'pyper_web_theme/static/src/core/**/*',
            'pyper_web_theme/static/src/views/**/*',
            'pyper_web_theme/static/src/webclient/**/*',
        ],
    },
}
