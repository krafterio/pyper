# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, models, Command


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    def _is_spreadsheet_dashboard_enabled(self):
        group = self.env.ref('spreadsheet_dashboard.group_dashboard_manager', raise_if_not_found=False)

        return group and group.active

    def _enable_spreadsheet_dashboard(self):
        # Enable security group of spreadsheet dashboard
        group = self.env.ref('spreadsheet_dashboard.group_dashboard_manager', raise_if_not_found=False)

        if group:
            group.active = True

    def _disable_spreadsheet_dashboard(self):
        # Remove spreadsheet dashboard security groups for all users
        group = self.env.ref('spreadsheet_dashboard.group_dashboard_manager', raise_if_not_found=False)

        if group:
            group.users = [Command.unlink(user.id) for user in group.users]
            group.active = False
