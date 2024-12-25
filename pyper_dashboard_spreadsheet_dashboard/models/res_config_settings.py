# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    dashboard_use_spreadsheet_dashboard = fields.Boolean(
        'Use Spreadsheet Dashboard?',
    )

    @api.model
    def get_values(self):
        res = super().get_values()
        res['dashboard_use_spreadsheet_dashboard'] = self.env['ir.ui.menu'].sudo()._is_spreadsheet_dashboard_enabled()

        return res

    def set_values(self):
        super().set_values()

        if self.dashboard_use_spreadsheet_dashboard:
            self.env['ir.ui.menu'].sudo()._enable_spreadsheet_dashboard()
        else:
            self.env['ir.ui.menu'].sudo()._disable_spreadsheet_dashboard()
