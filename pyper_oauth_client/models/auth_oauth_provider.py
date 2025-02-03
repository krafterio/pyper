# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models, _, fields, api


class AuthOauthProvider(models.Model):
    _inherit = 'auth.oauth.provider'

    type_user_create = fields.Selection([
        ('internal', 'Internal User'),
        ('portal', 'Portal User'),
    ], string='User Type', default='internal', required=True)

    client_secret = fields.Char('Secret Key', copy=False)
    token_endpoint = fields.Char('Token Endpoint', copy=False)
