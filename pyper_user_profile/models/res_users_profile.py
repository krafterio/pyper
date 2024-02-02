# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import _, fields, models, api
from odoo.exceptions import ValidationError

class Users(models.Model):
    _name = 'res.users.profile'
    _description = 'Profile for users defining their default access rights'

    name = fields.Char(required=True)

    is_default_profile = fields.Boolean('Is default profile', help='Is the default profile for newly created users')
    
    group_ids = fields.Many2many('res.groups', string='Default rights', compute='_compute_group_ids')

    role_ids = fields.Many2many(
        'res.users.role', 
        relation='res_users_profile_res_users_role_rel', 
        column1='profile_id', 
        column2='role_id', 
        string='Default roles'
    )

    user_ids = fields.One2many(
        'res.users', 'user_profile_id',
    )

    def _compute_group_ids(self):
        for rec in self:
            rec.group_ids = rec.role_ids.mapped('group_ids')

    @api.model_create_multi
    def create(self, vals_list):
        if any([vals.get('is_default_profile') for vals in vals_list]) \
                and self.search_count([('is_default_profile', '=', True)]):
            raise ValidationError(_('There is already a default profile. Please deactivate it first'))
        return super().create(vals_list)

    def write(self, vals):
        if vals.get('is_default_profile') and self.search_count([('is_default_profile', '=', True)]):
            raise ValidationError(_('There is already a default profile. Please deactivate it first'))
        return super().write(vals)
