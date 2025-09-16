# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import fields, models


class IrUIView(models.Model):
    _inherit = 'ir.actions.act_window.view'

    view_mode = fields.Selection(
        selection_add=[
            ('timeline', 'Timeline')
        ],
        ondelete={'timeline': 'cascade'},
    )
