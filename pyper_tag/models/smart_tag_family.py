# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, AccessError


class SmartTagFamily(models.Model):
    _name = 'smart.tag.family'
    _description = 'Gather several Tags'
    _order='is_public DESC, name'

    name = fields.Char(
        string="Family Name",
        required=True,
    )

    tag_ids = fields.One2many(
        'smart.tag', 
        'family_id', 
        string='Tags',
        domain="[('tag_model_name', '=', 'tag_model_name'), ('is_public', '=', 'is_public'), '|', ('is_public', '=', True), ('user_id', '=', uid)]",
        help="Tags associated in this family"
    )

    is_public = fields.Boolean(
        string='Is Public', 
        default=False,
        help='If checked, this familly tag will be visible to all users.'
    )

    tag_model_name = fields.Char(
        'Associated Model',
        store=True,
        readonly=True,
        index=True,
    )

    user_id = fields.Many2one(
        'res.users', 
        string='Created By', 
        default=lambda self: self.env.user,
        readonly=True
    )

    only_child = fields.Boolean(
        'Only child',
        default=True,
        help="If checked, you can't chose more than one child per family."
    )

    can_edit = fields.Boolean(
        string='Can edit',
        compute='_compute_can_edit',
        store=False
    )

    @api.depends('user_id', 'is_public')
    def _compute_can_edit(self):
        public_smart_tag_group = self.env.ref('pyper_tag.group_public_smart_tag_manager')
        for family in self:
            family.can_edit = not family.is_public or public_smart_tag_group in self.env.user.groups_id or self.env.user.has_group('base.group_system')

    @api.onchange('tag_ids')
    def _onchange_tag_model_name(self):
        for family in self:
            if not family.tag_model_name:
                if len(family.tag_ids) > 0:
                    family.tag_model_name = family.tag_ids[0].tag_model_name
                

    def action_open_family_tag_form(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'smart.tag.family',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
        }

    def write(self, vals):
        res = super(SmartTagFamily, self).write(vals)
        if 'is_public' in vals:
            if not self.env.user.has_group('base.group_system') or not self.env.user.has_group('pyper_tag.group_public_smart_tag_manager'):
                raise AccessError(_('Only administrators or public smart tag editors can change the visibility of public tag families.'))
            for family in self:
                for tag in family.tag_ids:
                    tag.is_public = vals['is_public']
        return res

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('is_public') and not self.env.user.has_group('base.group_system') or not self.env.user.has_group('pyper_tag.group_public_smart_tag_manager'):
                raise AccessError(_('Only administrators can create public tag families.'))
        return super(SmartTagFamily, self).create(vals_list)

    def unlink(self):
        for family in self:
            if family.is_public and not self.env.user.has_group('base.group_system'):
                raise AccessError(_('Only administrators can delete public tags.'))
            if family.is_public and not family.can_edit:
                raise AccessError(_('You need access to public smart tag group permission to delete a public tag.'))
        return super(SmartTagFamily, self).unlink()
