# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models, fields, api
import secrets


class OAuthToken(models.Model):
    _name = 'oauth.token'
    _description = 'OAuth Token'

    client_id = fields.Many2one('oauth.client', required=True, ondelete='cascade', string='Client')
    user_id = fields.Many2one('res.users', required=True, ondelete='cascade', string='User')
    token = fields.Char(required=True, index=True, unique=True, string='Access Token')
    refresh_token = fields.Many2one('oauth.refresh_token', required=True, ondelete='cascade', string='Refresh Token')
    expires_at = fields.Datetime(string='Expiration Time')
    scope = fields.Char(string='Scope', help='Permissions granted to this token')

    is_expired = fields.Boolean(compute='_compute_is_expired', string='Is Expired')

    @api.depends('expires_at')
    def _compute_is_expired(self):
        now = fields.Datetime.now()
        for record in self:
            record.is_expired = record.expires_at and record.expires_at < now
    
    def _generate_token(self):
        return secrets.token_urlsafe(64)
