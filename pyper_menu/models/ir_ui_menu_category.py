# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class IrUiMenuCategory(models.Model):
    _name = 'ir.ui.menu.category'
    _description = 'Menu category'
    _order = 'sequence asc, id asc'

    name = fields.Char(
        'Name',
        required=True,
        translate=True,
    )

    sequence = fields.Integer(
        'Sequence',
        default=100,
    )
