# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    res_users_settings_font_size = fields.Selection(
        related='res_users_settings_id.font_size',
        readonly=False,
        required=True,
    )

    @api.model
    def get_accessibility_scss_variables(self):
        return {
            'font-size': self.res_users_settings_font_size,
        }
