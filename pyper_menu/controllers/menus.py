# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import http
from odoo.http import request
from odoo.tools.safe_eval import safe_eval


class MenuItems(http.Controller):
    @http.route('/web/webclient/load_menu_counters', methods=['POST'], type='json', auth='user')
    def load_menu_counters(self, ids):
        menus = request.env['ir.ui.menu'].search([('id', 'in', ids)])
        values = {}

        for menu in menus:
            if menu.action and 'domain' in menu.action and menu.action.domain:
                action = menu.action
                values.update({menu.id: request.env[action.res_model].search_count(safe_eval(action.domain))})

        return {
            'menuCounters': values,
        }
