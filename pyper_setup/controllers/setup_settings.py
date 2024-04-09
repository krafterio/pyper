# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo.http import Controller, route, request


class SetupSettings(Controller):
    @route('/pyper_setup/settings', type='json', auth='user')
    def setup_settings(self, prefix=None):
        if not prefix:
            return []

        return request.env['ir.config_parameter'].sudo().search_read(
            [('key', 'like', str(prefix) + '%')],
            ['key', 'value'],
        )
