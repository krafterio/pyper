# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import _, api, fields, models, Command
from odoo.exceptions import RedirectWarning


class ResUsers(models.Model):
    _inherit = 'res.users'

    role_id = fields.Many2one(
        'res.groups',
        string='Role',
        domain=[('is_role', '=', True)],
        compute='_compute_role_id',
        inverse='_inverse_role_id',
        store=True,
    )

    role_ids = fields.Many2many(
        'res.groups',
        'res_users_role_rel',
        'uid',
        'rid',
        string='Extra roles',
        domain=[('is_role', '=', True)],
        inverse='_inverse_role_ids',
        store=True,
        help='Include the main role and allow to define other roles for this user',
    )

    has_custom_groups = fields.Boolean(
        'Has custom access rights?',
        compute='_compute_has_custom_groups',
        store=True,
    )

    @api.depends('groups_id', 'groups_id.implied_ids', 'role_ids')
    def _compute_role_id(self):
        for user in self:
            if not user.role_id or not user.role_ids or user.role_id.id not in user.role_ids.ids:
                user.role_id = user.role_ids[0] if user.role_ids else False

    def _inverse_role_id(self):
        for user in self:
            user.groups_id = user.groups_id.filtered(lambda g: not g.is_role)

            if user.role_id:
                user.groups_id |= user.role_id

    def _inverse_role_ids(self):
        for user in self:
            existing_groups = user.groups_id
            user.groups_id |= user.role_ids - existing_groups
            user.groups_id -= existing_groups.filtered(lambda g: g.is_role) - user.role_ids

        self._compute_role_id()

    @api.depends('groups_id', 'groups_id.implied_ids', 'role_ids')
    def _compute_has_custom_groups(self):
        for user in self:
            user.has_custom_groups = user.role_id and len(get_custom_groups(user)) > 0

    @api.onchange('role_id')
    def _onchange_role_id(self):
        for user in self:
            new_role_ids = [r.id for r in user.role_ids.filtered(lambda r: val_id(r) != val_id(user.role_id))]
            new_role_cmds = [Command.unlink(rid) for rid in new_role_ids]

            # Add new role in roles if defined
            if user.role_id and val_id(user.role_id) not in new_role_ids:
                new_role_cmds.append(Command.link(user.role_id.id))

            if new_role_cmds:
                user.role_ids = new_role_cmds

    def write(self, vals):
        res = super().write(vals)

        # Reset user security groups when main role is updated
        if 'role_id' in vals and vals['role_id'] != False:
            self._onchange_role_id()
            self.reset_security_groups()

        return res

    def action_show_groups(self):
        action = super().action_show_groups()
        tree_view_id = self.env.ref('pyper_security_role.view_groups_tree').id
        action['views'] = [(tree_view_id, 'tree')] + [
            view for view in action.get('views', []) if view[1] != 'tree'
        ]

        return action

    def action_show_custom_groups(self):
        action = self.action_show_groups()
        action.update({
            'domain': [('id', 'in', get_custom_groups(self).ids)],
            'target': 'new',
        })

        return action

    def action_confirm_reset_security_groups(self):
        raise RedirectWarning(
            _('Are you sure you want to reset access rights with only access rights defined in roles?'),
            self.env.ref('pyper_security_role.action_reset_security_groups').id,
            _('Reset access rights'),
            {**self.env.context},
        )

    def reset_security_groups(self):
        user_type_id = self.env.ref('base.module_category_user_type').id

        for user in self:
            kept_groups = user.groups_id.filtered(lambda g: g.is_role or g.category_id.id == user_type_id)
            implied_kept_groups = kept_groups

            for kept_group in kept_groups:
                implied_kept_groups |= kept_group.trans_implied_ids

            remove_groups = user.groups_id - implied_kept_groups
            user.groups_id = remove_groups.mapped(lambda g: Command.unlink(val_id(g)))

        return {
            'type': 'ir.actions.client',
            'tag': 'soft_reload',
        }


def val_id(r):
    return r.id.origin if isinstance(r.id, models.NewId) else r.id


def get_custom_groups(user):
    user_type = user.env.ref('base.module_category_user_type')
    user_type_group = user.groups_id.filtered(lambda g: g.category_id == user_type)

    roles_groups = user.role_ids + user.role_ids.trans_implied_ids
    user_groups = user.groups_id + user.groups_id.trans_implied_ids
    user_groups -= user_type_group
    user_groups -= user_type_group.trans_implied_ids

    return user_groups - roles_groups
