# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    hide_username_password_login = fields.Boolean(
        string="Disable Username/Password Login",
        config_parameter='oauth_client.hide_username_password_login'
    )
