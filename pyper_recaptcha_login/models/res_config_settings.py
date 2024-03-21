# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    recaptcha_login_enabled = fields.Boolean(
        string='Enabled reCAPTCHA login lockdown',
        config_parameter='pyper_recaptcha_login.enabled'
    )

    recaptcha_login_max_error_attempt = fields.Integer(
        string='Max Error Attempt',
        help="The maximum number of attempts before locking the login",
        config_parameter='pyper_recaptcha_login.max_error_attempt'
    )

    recaptcha_login_site_key = fields.Char(
        string='reCAPTCHA Site Key',
        help='The Site Key of your reCAPTCHA',
        config_parameter='pyper_recaptcha_login.site_key'
    )

    recaptcha_login_private_key = fields.Char(
        string='reCAPTCHA Private Key',
        help='The Private Key of your reCAPTCHA',
        config_parameter='pyper_recaptcha_login.private_key'
    )

    @api.model
    def enable_recaptcha_login(self):
        self.env['res.config.settings'].create({
            'recaptcha_login_enabled': True,
            'recaptcha_login_max_error_attempt': 2,
            'recaptcha_login_site_key': 'CHANGE_SITE_KEY',
            'recaptcha_login_private_key': 'CHANGE_PRIVATE_KEY',
        }).execute()
