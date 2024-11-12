# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    recaptcha_signup_enabled = fields.Boolean(
        string='Enabled reCAPTCHA signup lockdown',
        config_parameter='pyper_recaptcha_signup.enabled'
    )

    recaptcha_signup_site_key = fields.Char(
        string='Signup reCAPTCHA Site Key',
        help='The Site Key of your reCAPTCHA',
        config_parameter='pyper_recaptcha_signup.site_key'
    )

    recaptcha_signup_private_key = fields.Char(
        string='Signup reCAPTCHA Private Key',
        help='The Private Key of your reCAPTCHA',
        config_parameter='pyper_recaptcha_signup.private_key'
    )

    recaptcha_signup_min_score = fields.Float(
        "Signup reCAPTCHA minimum score",
        help="By default, should be one of 0.1, 0.3, 0.7, 0.9.\n1.0 is very likely a good interaction, 0.0 is very likely a bot",
        default="0.7",
        config_parameter='pyper_recaptcha_signup.min_score',
    )

    @api.constrains('recaptcha_signup_min_score')
    def _check_recaptcha_signup_min_score(self):
        for record in self:
            if not (0.0 <= record.recaptcha_signup_min_score <= 1.0):
                raise ValidationError(
                    _('Minimum reCAPTCHA score must be inside 0.0 - 1.0 range')
                )
