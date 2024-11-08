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
