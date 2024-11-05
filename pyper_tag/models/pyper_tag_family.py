# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class PyperTagFamily(models.Model):
    _name = 'pyper.tag.family'
    _description = 'Gather several Tags'

    name = fields.Char(
        string="Family Name",
        required=True,
    )

    tag_ids = fields.One2many(
        'pyper.tag', 
        'family_id', 
        string="Tags",
        domain="[('tag_model_name', '=', 'tag_model_name'), ('is_public', '=', 'is_public'), '|', ('is_public', '=', True), ('user_id', '=', uid)]",
        help="Tags associated in this family"
    )

    is_public = fields.Boolean(
        string="Is Public", 
        default=False,
        readonly=True, 
        help="If checked, this familly tag will be visible to all users."
    )

    tag_model_name = fields.Char(
        'Associated Model',
        readonly=True,
    )

    user_id = fields.Many2one(
        'res.users', 
        string="Created By", 
        default=lambda self: self.env.user,
        readonly=True
    )

    # @api.onchange('is_public')
    # def _onchange_is_public(self):
    #     for tag in self.tag_ids:
    #         tag.is_public = self.is_public

    # @api.constrains('tag_ids', 'tag_model_name', 'is_public')
    # def _check_tags_family_traits(self):
    #     for family in self:
    #         if family.tag_ids:
    #             tag_model_names = {tag.tag_model_name for tag in family.tag_ids}
    #             if len(tag_model_names) > 1:
    #                 raise ValidationError("All tags in the same family must have the same 'Associated Model'.")

    #             if not family.tag_model_name:
    #                 family.tag_model_name = family.tag_ids[0].tag_model_name
    #             else:
    #                 for tag in family.tag_ids:
    #                     tag.tag_model_name = family.tag_model_name
    #             if any(tag.is_public != family.is_public for tag in family.tag_ids):
    #                 raise ValidationError("All tags in the same family must be either all public or all private.")
