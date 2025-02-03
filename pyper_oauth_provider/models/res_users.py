# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models


class ResUsers(models.Model):
    _inherit = 'res.users'

    def action_revoke_user(self, vals):
        token = self.env['oauth.token'].search([('user_id', '=', self.id)])
        token.unlink()