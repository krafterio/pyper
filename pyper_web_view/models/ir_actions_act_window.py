# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class IrUiView(models.Model):
    _inherit = 'ir.actions.act_window'

    ir_views_id = fields.Many2one(
        'ir.views',
        string='Saved views',
        ondelete='cascade',
    )
