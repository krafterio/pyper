# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    overlay_menu_show_root_app = fields.Boolean(
        'Show only root menu items?',
        config_parameter='pyper_overlay_menu.overlay_menu_props.showRootApp',
    )

    overlay_menu_hide_empty_category = fields.Boolean(
        'Hide empty categories?',
        config_parameter='pyper_overlay_menu.overlay_menu_props.hideEmptyCategory',
    )
