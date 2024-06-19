# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    child_ids = fields.One2many(
        'product.product',
        'product_tmpl_id',
        'Variants'
    )
