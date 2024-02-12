# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

{
    'name': 'Pyper',
    'category': 'Hidden/Tools',
    'license': 'Other proprietary',
    'description': 'Pyper addons superset to build .',
    'version': '1.0',
    'author': 'Krafter SAS',
    'maintainer': [
        'Krafter SAS',
    ],
    'website': 'https://krafter.io',
    'installable': True,
    'depends': [
        'base_setup',
        'web',
    ],
    'data': [
        'views/webclient_templates.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            # TODO Remove deprecated assets
            ('before', 'web/static/src/scss/primary_variables.scss', 'pyper/static/src/scss/primary_variables.scss'),
            ('before', 'web/static/src/**/*.variables.scss', 'pyper/static/src/**/*.variables.scss'),
        ],
        'web._assets_secondary_variables': [
            # TODO Remove deprecated assets
            ('before', 'web/static/src/scss/secondary_variables.scss', 'pyper/static/src/scss/secondary_variables.scss'),
        ],
        'web._assets_backend_helpers': [
            # TODO Remove deprecated assets
            ('before', 'web/static/src/scss/bootstrap_overridden.scss', 'pyper/static/src/scss/bootstrap_overridden.scss'),
        ],
        'web.assets_backend': [
            'pyper/static/src/core/ui/**/*',
            'pyper/static/src/views/fields/**/*',

            # TODO Remove deprecated assets
            ('before', 'web/static/src/legacy/scss/fields.scss', 'pyper/static/src/legacy/scss/fields.scss'),
            'pyper/static/src/legacy/scss/control_panel_mobile.scss',
            'pyper/static/src/legacy/scss/dropdown.scss',
            'pyper/static/src/legacy/scss/touch_device.scss',
            'pyper/static/src/legacy/scss/modal_mobile.scss',
            'pyper/static/src/views/kanban/**/*',
            'pyper/static/src/views/list/**/*',
            'pyper/static/src/views/pivot/**/*',
            'pyper/static/src/core/form_renderer/**/*',
            'pyper/static/src/core/notebook/**/*',
            'pyper/static/src/core/notifications/**/*',
            'pyper/static/src/webclient/**/*',
        ],
    },
}
