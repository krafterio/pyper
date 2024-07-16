# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class DashboardBoardItem(models.Model):
    _name = 'dashboard.dashboard'
    _description = 'Dashboard'
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

    view_id = fields.Many2one(
        'ir.ui.view',
        string='Original View',
        index=True,
        required=False,
        ondelete='cascade',
        domain=[('model', '=', 'dashboard.dashboard'), ('type', '=', 'qweb')],
    )

    is_editable = fields.Boolean(
        'Is editable?',
        compute='_compute_is_editable',
        store=True,
    )

    arch_db = fields.Text(
        'Custom architecture',
        required=False,
    )

    arch = fields.Text(
        'Architecture',
        compute='_compute_arch',
        inverse='_inverse_arch',
    )

    @api.depends('view_id')
    def _compute_is_editable(self):
        for board in self:
            board.is_editable = board.view_id.id is False

    @api.depends('arch_db', 'view_id')
    def _compute_arch(self):
        for board in self:
            board.arch = board.arch_db or board.view_id.arch

    def _inverse_arch(self):
        for board in self:
            if board.arch:
                board.arch_db = board.arch

            if board.arch_db and board.view_id.arch and board.arch_db == self._arch_preprocessing(board.view_id.arch):
                board.arch_db = False

    def write(self, vals):
        if 'arch_db' in vals or 'arch' in vals:
            for board in self:
                if board.view_id:
                    raise UserError(_('Unable to override this dashboard because it is associated with a view'))

        return super().write(vals)

    def unlink(self):
        for board in self:
            if board.view_id:
                raise UserError(_('Unable to delete this dashboard because it is associated with a view'))

        return super().unlink()

    @api.onchange('view_id')
    def _onchange_view_id(self):
        for board in self:
            board.arch_db = False

    @api.model
    def get_view(self, view_id=None, view_type='form', **options):
        """
        Overrides orm field_view_get.
        @return: Dictionary of Fields, arch and toolbar.
        """
        res = super().get_view(view_id, view_type, **options)

        if view_type == 'form':
            res['arch'] = self._arch_preprocessing(res['arch'])

        return res

    @api.model
    def _arch_preprocessing(self, arch):
        from lxml import etree

        def remove_unauthorized_children(node):
            for child in node.iterchildren():
                if child.tag == 'action' and child.get('invisible'):
                    node.remove(child)
                else:
                    remove_unauthorized_children(child)

            return node

        arch_node = etree.fromstring(arch)

        # Add the js_class 'dashboard' on the fly to force the webclient to instantiate a DashboardView
        # instead of FormView
        if len(arch_node.findall('.//dashboard')):
            arch_node.set('js_class', 'dashboard')

        return etree.tostring(remove_unauthorized_children(arch_node), pretty_print=True, encoding='unicode')

    def action_dashboard_debug_view(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'dashboard.dashboard',
            'res_id': self.id,
            'view_mode': 'form',
            'view_id': self.env.ref('pyper_dashboard.view_dashboard_dashboard_form').id,
        }
