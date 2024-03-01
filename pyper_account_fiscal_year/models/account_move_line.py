# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    date_range_fy_id = fields.Many2one(
        related='move_id.date_range_fy_id',
        store=True,
    )
