# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models, _, fields


class OAuthScope(models.Model):
    _name = 'oauth.scope'
    _description = 'OAuth2 Scopes'

    name = fields.Char(required=True, string="Scope Name", help="The technical name of the scope (e.g., openid, email).")
    description = fields.Text(string="Description", help="Details about what this scope provides access to separated by commas.")
