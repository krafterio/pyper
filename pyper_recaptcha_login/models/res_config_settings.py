# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    recaptcha_login_enabled = fields.Boolean(
        string='Enabled reCAPTCHA login lockdown',
        config_parameter='pyper_recaptcha_login.enabled'
    )

    recaptcha_login_site_key = fields.Char(
        string='Login reCAPTCHA Site Key',
        help='The Site Key of your reCAPTCHA',
        config_parameter='pyper_recaptcha_login.site_key'
    )

    recaptcha_login_private_key = fields.Char(
        string='Login reCAPTCHA Private Key',
        help='The Private Key of your reCAPTCHA',
        config_parameter='pyper_recaptcha_login.private_key'
    )

    recaptcha_login_min_score = fields.Float(
        "Login minimum score",
        help="By default, should be one of 0.1, 0.3, 0.7, 0.9.\n1.0 is very likely a good interaction, 0.0 is very likely a bot",
        default="0.7",
        config_parameter='pyper_recaptcha_login.min_score',
    )

    @api.constrains('recaptcha_login_min_score')
    def _check_recaptcha_login_min_score(self):
        for record in self:
            if not (0.0 <= record.recaptcha_login_min_score <= 1.0):
                raise ValidationError(
                    _('Minimum reCAPTCHA score must be inside 0.0 - 1.0 range')
                )
