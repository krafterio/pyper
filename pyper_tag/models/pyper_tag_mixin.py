# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class PyperTagMixin(models.AbstractModel):
    _name = 'pyper.tag.mixin'
    _description = 'Pyper Tag Mixin'

    pyper_tag_ids = fields.Many2many(
        'pyper.tag',
        string='Tags', 
    )

    tag_model_name = fields.Char(
        'Associated tag model name',
        compute='_compute_tag_model_name',
    )

    def _compute_tag_model_name(self):
        for mixin in self:
            mixin.tag_model_name = self._name

    @api.onchange('pyper_tag_ids')
    def _only_one_tag_per_family(self):
        for mixin in self:
            if mixin.pyper_tag_ids:
                unique_tags_by_family = {}
                for tag in mixin.pyper_tag_ids:
                    family_id = tag.family_id
                    if family_id in unique_tags_by_family:
                        mixin.pyper_tag_ids -= unique_tags_by_family[family_id]
                    unique_tags_by_family[family_id] = tag
