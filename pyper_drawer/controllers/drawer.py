# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo.http import Controller, route, request


class Drawer(Controller):
    @route('/drawer/settings', type='json', auth='user')
    def drawer_settings(self):
        return request.env['ir.config_parameter'].sudo().search_read(
            [('key', 'like', 'pyper_drawer.drawer_props.%')],
            ['key', 'value'],
        )
