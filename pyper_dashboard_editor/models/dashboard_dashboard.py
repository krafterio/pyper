# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class DashboardBoardItem(models.Model):
    _inherit = 'dashboard.dashboard'

    arch_db = fields.Text(
        'Custom architecture',
        required=False,
    )

    @api.depends('arch_db', 'view_id')
    def _compute_arch(self):
        super()._compute_arch()

        for board in self:
            if board.arch_db:
                board.arch = board.arch_db

    def _inverse_arch(self):
        super()._inverse_arch()

        for board in self:
            if board.arch:
                board.arch_db = board.arch

            if board.arch_db and board.view_id.arch and board.arch_db == self._arch_preprocessing(board.view_id.arch):
                board.arch_db = False

    def write(self, vals):
        if 'arch_db' in vals:
            for board in self:
                if board.view_id:
                    raise UserError(_('Unable to override this dashboard because it is associated with a view'))

        return super().write(vals)

    @api.onchange('view_id')
    def _onchange_view_id(self):
        for board in self:
            board.arch_db = False
