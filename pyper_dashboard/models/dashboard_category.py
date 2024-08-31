# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class DashboardCategory(models.Model):
    _name = 'dashboard.category'
    _description = 'Dashboard category'
    _order = 'sequence ASC, id ASC'

    active = fields.Boolean(
        string='Active',
        default=True,
    )

    def _default_sequence(self):
        return (self.search([], order='sequence desc', limit=1).sequence or 0) + 1

    sequence = fields.Integer(
        'Sequence',
        default=_default_sequence,
    )

    name = fields.Char(
        'Name',
        required=True,
        translate=True,
    )
