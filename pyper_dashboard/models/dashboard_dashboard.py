# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.osv import expression


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

    full_name = fields.Char(
        string='Dashboard Name',
        compute='_compute_full_name',
        search='_search_full_name',
    )

    category_id = fields.Many2one(
        'dashboard.category',
        string='Category',
        index=True,
    )

    category_sequence = fields.Integer(
        string='Category sequence',
        related='category_id.sequence',
        store=True,
    )

    group_ids = fields.Many2many(
        'res.groups',
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

    arch = fields.Text(
        'Architecture',
        compute='_compute_arch',
        inverse='_inverse_arch',
    )

    @api.depends('category_id.name', 'name')
    def _compute_full_name(self):
        # Important: value must be stored in environment of board, not board1!
        for board, board1 in zip(self, self.sudo()):
            if board1.category_id:
                board.full_name = '%s / %s' % (board1.category_id.name, board1.name)
            else:
                board.full_name = board1.name

    def _search_full_name(self, operator, operand):
        lst = True

        if isinstance(operand, bool):
            return [[('name', operator, operand)]]

        if isinstance(operand, str):
            lst = False
            operand = [operand]

        where = []

        for group in operand:
            values = [v for v in group.split('/') if v]
            group_name = values.pop().strip()
            category_name = values and '/'.join(values).strip() or group_name
            group_domain = [('name', operator, lst and [group_name] or group_name)]
            category_ids = self.env['dashboard.category'].sudo()._search(
                [('name', operator, [category_name] if lst else category_name)])
            category_domain = [('category_id', 'in', category_ids)]

            if operator in expression.NEGATIVE_TERM_OPERATORS and not values:
                category_domain = expression.OR([category_domain, [('category_id', '=', False)]])

            if (operator in expression.NEGATIVE_TERM_OPERATORS) == (not values):
                sub_where = expression.AND([group_domain, category_domain])
            else:
                sub_where = expression.OR([group_domain, category_domain])

            if operator in expression.NEGATIVE_TERM_OPERATORS:
                where = expression.AND([where, sub_where])
            else:
                where = expression.OR([where, sub_where])

        return where

    @api.depends('view_id')
    def _compute_is_editable(self):
        for board in self:
            board.is_editable = board.view_id.id is False

    @api.depends('view_id')
    def _compute_arch(self):
        for board in self:
            board.arch = board.view_id.arch

    def _inverse_arch(self):
        pass

    def write(self, vals):
        if 'arch' in vals:
            for board in self:
                if board.view_id:
                    raise UserError(_('Unable to override this dashboard because it is associated with a view'))

        return super().write(vals)

    def unlink(self):
        for board in self:
            if board.view_id:
                raise UserError(_('Unable to delete this dashboard because it is associated with a view'))

        return super().unlink()

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
