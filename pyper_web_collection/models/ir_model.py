# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import fields, models


class IrCollection(models.Model):
    _inherit = 'ir.model'

    is_collectionable = fields.Boolean(
        'Is collectionable ?',
        readonly=True,
    )

    def _reflect_model_params(self, model):
        vals = super()._reflect_model_params(model)
        vals['is_collectionable'] = model._name != 'collection.mixin' and isinstance(model, self.pool['collection.mixin'])

        return vals
