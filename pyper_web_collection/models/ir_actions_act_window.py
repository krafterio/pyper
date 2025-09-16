# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import api, fields, models


class IrActionsActWindow(models.Model):
    _inherit = 'ir.actions.act_window'

    ir_collections_id = fields.Many2one(
        'ir.collections',
        string='Collection',
        ondelete='cascade',
    )

    @api.depends('ir_collections_id.name')
    def _compute_display_name(self):
        for rec in self:
            if rec.ir_collections_id:
                rec.display_name = rec.ir_collections_id.name
            else:
                super(IrActionsActWindow, rec)._compute_display_name()
