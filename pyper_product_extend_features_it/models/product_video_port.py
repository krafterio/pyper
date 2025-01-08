# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models

class ProductVideoPort(models.Model):
    _name = 'product.video.port'
    _description = 'Product video port'
    _order = 'sequence ASC'

    sequence = fields.Integer(string='Sequence')

    name = fields.Char(string='Name')
