# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    recaptcha_signup_enabled = fields.Boolean(
        string='Enabled reCAPTCHA signup lockdown',
        config_parameter='pyper_recaptcha_signup.enabled'
    )

    recaptcha_signup_max_error_attempt = fields.Integer(
        string='Max Error Attempt',
        help="The maximum number of attempts before locking the signup",
        config_parameter='pyper_recaptcha_signup.max_error_attempt'
    )

    recaptcha_signup_site_key = fields.Char(
        string='reCAPTCHA Site Key',
        help='The Site Key of your reCAPTCHA',
        config_parameter='pyper_recaptcha_signup.site_key'
    )

    recaptcha_signup_private_key = fields.Char(
        string='reCAPTCHA Private Key',
        help='The Private Key of your reCAPTCHA',
        config_parameter='pyper_recaptcha_signup.private_key'
    )

    @api.model
    def enable_recaptcha_signup(self):
        self.env['res.config.settings'].create({
            'recaptcha_signup_enabled': True,
            'recaptcha_signup_max_error_attempt': 2,
            'recaptcha_signup_site_key': 'CHANGE_SITE_KEY',
            'recaptcha_signup_private_key': 'CHANGE_PRIVATE_KEY',
        }).execute()
