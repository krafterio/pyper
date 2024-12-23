# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    sync_all_fetchmail_server_ids = fields.One2many(
        'fetchmail.server',
        'user_id',
        'Fetch Mail Servers',
        domain=lambda self: [('user_id', '=', self.id), ('sync_all', '=', True)],
        ondelete='cascade',
    )
