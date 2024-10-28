# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class PyperTagMixin(models.AbstractModel):
    _name = 'pyper.tag.mixin'
    _description = 'Pyper Tag Mixin'

    tag_ids = fields.Many2many(
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
