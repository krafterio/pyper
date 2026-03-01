# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo.addons.web.controllers.action import Action
from odoo.http import route


class DashboardAction(Action):

    @route('/web/action/load_breadcrumbs', type='jsonrpc', auth='user', readonly=True)
    def load_breadcrumbs(self, actions):
        results = super().load_breadcrumbs(actions)

        for i, (action_info, result) in enumerate(zip(actions, results)):
            if result.get('display_name') is not None or 'error' in result:
                continue

            action_id = action_info.get('action')
            if not action_id:
                continue

            try:
                act = self.load(action_id)
                name = act.get('display_name') or act.get('name')
                if name:
                    results[i] = {'display_name': name}
            except Exception:
                pass

        return results
