# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class CollectionMixin(models.AbstractModel):
    _name = 'collection.mixin'
    _description = 'Collection Mixin'

    collection_ids = fields.Many2many(
        'ir.collections',
        string='Collections',
        domain=lambda self: [('res_model_name', '=', self._name)],
        readonly=True,
    )
