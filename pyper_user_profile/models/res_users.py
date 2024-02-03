# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models, Command


class Users(models.Model):
    _inherit = 'res.users'

    def _default_profile(self):
        return (self.env['res.users.profile'].search([('is_default_profile', '=', True)], limit=1)
                or self.env.ref('pyper_user_profile.admin_profile', raise_if_not_found=False))

    user_profile_id = fields.Many2one(
        'res.users.profile',
        string='User profile',
        default=_default_profile,
    )

    user_role_ids = fields.Many2many(
        'res.users.role',
        relation='res_users_res_users_role_rel',
        column1='user_id',
        column2='role_id',
    )

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        res.apply_user_profile(force=True)

        return res

    def write(self, vals):
        old_roles = {
            user.id: user.user_role_ids 
            for user in self
        } if 'user_role_ids' in vals.keys() else None

        res = super().write(vals)

        if vals.get('user_profile_id'):
            self.apply_user_profile()

        if vals.get('user_role_ids'):
            for rec in self:
                new_roles = rec.user_role_ids
                added_roles = new_roles - old_roles[rec.id]
                removed_roles = old_roles[rec.id] - new_roles
                rec.apply_roles(added_roles)
                rec.remove_role(removed_roles)

        return res

    def apply_user_profile(self, force=False):
        """
        Apply the profile to the given user : Add the roles of the profile and their groups on the user.
        If force is True, the user's roles and groups will be cleared beforehand. 
        """
        for rec in self.filtered(lambda user: user.user_profile_id):
            roles = []

            if force:
                roles.append(Command.clear())

            for role in self.user_profile_id.role_ids:
                roles.append(Command.link(role.id))

            rec.write({
                'user_role_ids': roles,
            })

        return True

    def apply_roles(self, roles=None):
        """
        Apply given roles to add new groups. Roles must be currently one of the users roles.
        If no role is given, will reapply all roles.
        """
        for rec in self:
            rec.write({
                'groups_id': [Command.link(group.id) for group in roles.group_ids],
            })
    
    def remove_role(self, roles=None):
        """
        Remove given roles groups from user except if the user is still eligible to the group
        thanks to another role.
        If no role is given, will clear all roles.
        """
        for rec in self:
            groups_to_remove = self.env['res.groups']

            for group in roles.group_ids:
                if group not in rec.user_role_ids.group_ids:
                    groups_to_remove |= group

            if groups_to_remove:
                rec.write({
                    'groups_id': [Command.unlink(group.id) for group in groups_to_remove],
                })
