# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class PyperTagMixin(models.AbstractModel):
    _name = 'pyper.tag.mixin'
    _description = 'Pyper Tag Mixin'

    tag_ids = fields.Many2many(
        'smart.tag',
        string='Tags', 
    )

    tag_family_id = fields.Many2one(
        related='tag_ids.family_id',
        string='Tag Families',
    )

    tag_model_name = fields.Char(
        'Associated tag model name',
        default=lambda self: self._name,
        readonly=True,
        index=True,
    )

    def _compute_tag_model_name(self):
        for mixin in self:
            mixin.tag_model_name = self._name

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['tag_model_name'] = self._name
        return super().create(vals_list)

    @api.onchange('tag_ids')
    def _only_one_tag_per_family(self):
        for mixin in self:
            if mixin.tag_ids:
                unique_tags_by_family = {}
                for tag in mixin.tag_ids:
                    if tag.family_id:
                        family_id = tag.family_id
                        if family_id in unique_tags_by_family:
                            mixin.tag_ids -= unique_tags_by_family[family_id]
                        unique_tags_by_family[family_id] = tag
