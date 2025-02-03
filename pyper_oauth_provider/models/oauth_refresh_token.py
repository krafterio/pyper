# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models, fields, api


class OAuthRefreshToken(models.Model):
    _name = 'oauth.refresh_token'
    _description = 'OAuth Refresh Token'

    token = fields.Char(string='Refresh Token')
    expires_at = fields.Datetime(string='Expiration Time')
    is_expired = fields.Boolean(compute='_compute_is_expired', string='Is Expired')

    @api.depends('expires_at')
    def _compute_is_expired(self):
        now = fields.Datetime.now()
        for record in self:
            record.is_expired = record.expires_at and record.expires_at < now
