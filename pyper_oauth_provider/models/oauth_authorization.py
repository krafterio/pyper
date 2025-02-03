# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models, fields, api


class OAuthAuthorization(models.Model):
    _name = 'oauth.authorization'
    _description = 'OAuth Authorization'

    token = fields.Char(required=True, index=True, unique=True, string='Access Token')
