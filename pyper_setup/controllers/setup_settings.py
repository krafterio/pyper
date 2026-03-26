# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo.http import Controller, route, request
from odoo.orm.domains import Domain


class SetupSettings(Controller):
    @route('/pyper_setup/settings', type='jsonrpc', auth='user')
    def setup_settings(self, prefix=None):
        if not prefix:
            return []

        prefixes = prefix.split('|')
        domains = []

        for prefix in prefixes:
            domains.append([('key', 'like', str(prefix) + '%')])

        return request.env['ir.config_parameter'].sudo().search_read(
            Domain.OR(domains),
            ['key', 'value'],
        )
