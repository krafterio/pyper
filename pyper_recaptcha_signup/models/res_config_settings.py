# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    recaptcha_signup_enabled = fields.Boolean(
        string='reCAPTCHA on signup',
        config_parameter='pyper_recaptcha_signup.enabled'
    )
