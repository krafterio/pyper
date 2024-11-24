# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    recaptcha_login_enabled = fields.Boolean(
        string='reCAPTCHA on login',
        config_parameter='pyper_recaptcha_login.enabled'
    )
