# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models

class ProductScreenFormat(models.Model):
    _name = 'product.screen.format'
    _description = 'Product screen format'
    _order = 'sequence ASC'

    sequence = fields.Integer(string='Sequence')

    name = fields.Char(string='Name')
