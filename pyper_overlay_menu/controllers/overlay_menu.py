# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo.http import Controller, route, request


class OverlayMenu(Controller):
    @route('/overlay_menu/settings', type='json', auth='user')
    def overlay_menu_settings(self):
        return request.env['ir.config_parameter'].sudo().search_read(
            [('key', 'like', 'pyper_overlay_menu.overlay_menu_props.%')],
            ['key', 'value'],
        )
