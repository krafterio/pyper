# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import _, api, fields, models, Command
from odoo.exceptions import RedirectWarning


class ResUsers(models.Model):
    _inherit = 'res.users'

    security_role_id = fields.Many2one(
        'res.groups',
        string='Security Role',
        compute='_compute_security_role_id',
        inverse='_inverse_security_role_id',
        store=True,
    )

    security_role_ids = fields.Many2many(
        'res.groups',
        'res_users_security_role_rel',
        'uid',
        'rid',
        string='Extra roles',
        help='Include the main role and allow to define other roles for this user',
    )

    has_custom_groups = fields.Boolean(
        'Has custom access rights?',
        compute='_compute_has_custom_groups',
        store=True,
    )

    @api.depends('group_ids', 'group_ids.implied_ids', 'security_role_ids')
    def _compute_security_role_id(self):
        for user in self:
            if not user.security_role_id or not user.security_role_ids or user.security_role_id.id not in user.security_role_ids.ids:
                user.security_role_id = user.security_role_ids[0] if user.security_role_ids else False

    def _inverse_security_role_id(self):
        for user in self:
            user.group_ids = user.group_ids.filtered(lambda g: not g.is_role)

            if user.security_role_id:
                user.group_ids |= user.security_role_id

    def _inverse_security_role_ids(self):
        for user in self:
            existing_groups = user.group_ids
            user.group_ids |= user.security_role_ids - existing_groups
            user.group_ids -= existing_groups.filtered(lambda g: g.is_role) - user.security_role_ids

        self._compute_security_role_id()

    @api.depends('group_ids', 'group_ids.implied_ids', 'security_role_ids')
    def _compute_has_custom_groups(self):
        for user in self:
            user.has_custom_groups = user.security_role_id and len(get_custom_groups(user)) > 0

    @api.onchange('security_role_id')
    def _onchange_security_role_id(self):
        for user in self:
            new_role_ids = [r.id for r in user.security_role_ids.filtered(lambda r: val_id(r) != val_id(user.security_role_id))]
            new_role_cmds = [Command.unlink(rid) for rid in new_role_ids]

            # Add new role in roles if defined
            if user.security_role_id and val_id(user.security_role_id) not in new_role_ids:
                new_role_cmds.append(Command.link(user.security_role_id.id))

            if new_role_cmds:
                user.security_role_ids = new_role_cmds

    def write(self, vals):
        res = super().write(vals)

        # Reset user security groups when main role is updated
        if 'security_role_id' in vals and vals['security_role_id'] != False:
            self._onchange_security_role_id()
            self.reset_security_groups()

        return res

    def action_show_groups(self):
        action = super().action_show_groups()
        tree_view_id = self.env.ref('pyper_security_role.view_groups_tree').id
        action['views'] = [(tree_view_id, 'list')] + [
            view for view in action.get('views', []) if view[1] != 'list'
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
        user_type_groups = self.env['res.groups']._get_user_type_groups()

        for user in self:
            kept_groups = user.group_ids.filtered(lambda g: g.is_role or g in user_type_groups)
            implied_kept_groups = kept_groups

            for kept_group in kept_groups:
                implied_kept_groups |= kept_group.trans_implied_ids

            remove_groups = user.group_ids - implied_kept_groups
            user.group_ids = remove_groups.mapped(lambda g: Command.unlink(val_id(g)))

        return {
            'type': 'ir.actions.client',
            'tag': 'soft_reload',
        }


def val_id(r):
    return r.id.origin if isinstance(r.id, models.NewId) else r.id


def get_custom_groups(user):
    user_type_groups = user.env['res.groups']._get_user_type_groups()
    user_type_group = user.group_ids & user_type_groups

    roles_groups = user.security_role_ids + user.security_role_ids.trans_implied_ids
    user_groups = user.group_ids + user.group_ids.trans_implied_ids
    user_groups -= user_type_group
    user_groups -= user_type_group.trans_implied_ids

    return user_groups - roles_groups
