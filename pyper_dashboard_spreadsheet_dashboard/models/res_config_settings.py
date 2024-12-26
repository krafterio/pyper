# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models, Command


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    dashboard_use_spreadsheet_dashboard = fields.Boolean(
        'Use Spreadsheet Dashboard?',
    )

    @api.model
    def get_values(self):
        res = super().get_values()
        res['dashboard_use_spreadsheet_dashboard'] = self.sudo()._is_spreadsheet_dashboard_enabled()

        return res

    def set_values(self):
        super().set_values()

        if self.dashboard_use_spreadsheet_dashboard:
            self.sudo()._enable_spreadsheet_dashboard()
        else:
            self.sudo()._disable_spreadsheet_dashboard()

    @api.model
    def _is_spreadsheet_dashboard_enabled(self):
        group = self.env.ref('spreadsheet_dashboard.group_dashboard_manager', raise_if_not_found=False)

        return group and group.active

    def _enable_spreadsheet_dashboard(self):
        # Enable security group of spreadsheet dashboard
        group = self.env.ref('spreadsheet_dashboard.group_dashboard_manager', raise_if_not_found=False)

        if group:
            group.active = True
            group._update_user_groups_view()
            self.env.registry.clear_cache()

    def _disable_spreadsheet_dashboard(self):
        # Remove spreadsheet dashboard security groups for all users
        group = self.env.ref('spreadsheet_dashboard.group_dashboard_manager', raise_if_not_found=False)

        if group:
            group.users = [Command.unlink(user.id) for user in group.users]
            group.active = False
            group._update_user_groups_view()
            self.env.registry.clear_cache()
