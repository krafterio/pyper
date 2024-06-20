# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api, _

class ProductCategory(models.Model):
    _inherit = 'product.category'

    is_book = fields.Boolean(
        'Is book',
        help=_('This field will add book properties on product sheet'),
    )
