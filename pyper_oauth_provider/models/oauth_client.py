# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models, fields
import secrets


class OAuthClient(models.Model):
    _name = 'oauth.client'
    _description = 'OAuth Client'

    name = fields.Char(required=True)
    client_id = fields.Char(
        required=True,
        unique=True,
        default=lambda self: self._generate_client_id()
    )
    redirect_uris = fields.Text(help="Comma-separated list of redirect URIs")
    scopes = fields.Text(help="Comma-separated list of scopes")
    skip_authorization = fields.Boolean(
        string='Skip Authorization',
        help='If enabled, the user will not be asked to authorize the client',
        default=False
    )
    client_secret = fields.Char(
        required=True,
        default=lambda self: self._generate_secret()
    )
    user_ids = fields.Many2many('res.users', string='Users')

    def write(self, vals):
        if 'user_ids' in vals:
            removed_user_ids = set()
            for command in vals['user_ids']:
                if command[0] == 3:
                    removed_user_ids.add(command[1])
            if removed_user_ids:
                tokens = self.env['oauth.token'].search([
                    ('client_id', '=', self.id),
                    ('user_id', 'in', list(removed_user_ids))
                ])
                for token in tokens:
                    token.refresh_token.unlink()
                    token.unlink()
        return super().write(vals)

    @staticmethod
    def _generate_secret():
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def _generate_client_id():
        return secrets.token_urlsafe(16)
