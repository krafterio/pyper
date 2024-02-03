# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, Command


class Users(models.Model):
    _name = 'res.users.role'
    _description = 'Role containing groups/rights that should be applied to all its member'

    name = fields.Char(
        required=True,
        translate=True,
    )

    notes = fields.Char()

    group_ids = fields.Many2many(
        'res.groups',
        string='Default rights',
    )

    user_ids = fields.Many2many(
        'res.users',
        relation='res_users_res_users_role_rel',
        column1='role_id',
        column2='user_id',
    )

    profile_ids = fields.Many2many(
        'res.users.profile',
        relation='res_users_profile_res_users_role_rel',
        column1='role_id',
        column2='profile_id',
    )

    def write(self, vals):
        old_groups = {
            role.id: role.group_ids 
            for role in self
        } if 'group_ids' in vals.keys() else None

        old_users = {
            role.id: role.user_ids
            for role in self
        } if 'user_ids' in vals.keys() else None

        res = super().write(vals)

        # Update changed users with all our role groups. We might need to use old/new group data
        # depending on command used
        if 'user_ids' in vals.keys():
            for rec in self:
                new_users = rec.user_ids
                added_users = new_users - old_users[rec.id]
                removed_users = old_users[rec.id] - new_users
                added_users.write({
                    'groups_id': [Command.link(rec.id)]
                })

                for group in old_groups[rec.id]:
                    non_eligible_users = removed_users.filtered(
                        lambda user: group not in user.user_role_ids.group_ids)
                    non_eligible_users.write({
                        'groups_id' : [Command.unlink(group.id)]
                    })

        # Default role groups were modified, so we need to update linked users
        # comparing records data pre and post write is slower, but allows us to handle more easily
        # cases where we use something else than Command.Link or Command.unlink
        if 'group_ids' in vals.keys():
            for rec in self:
                new_groups = rec.group_ids
                added_groups = new_groups - old_groups[rec.id]
                removed_groups = old_groups[rec.id] - new_groups

                # Simply add new groups to all users.
                rec.user_ids.write({
                    'groups_id': [Command.link(group.id) for group in added_groups]
                })

                # For removed groups, we need to check wether users are still eligible 
                # thanks to another role
                for group in removed_groups:
                    non_eligible_users = rec.user_ids.filtered(
                        lambda user: group not in user.user_role_ids.group_ids)
                    non_eligible_users.write({
                        'groups_id' : [Command.unlink(group.id)]
                    })
        return res
