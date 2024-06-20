# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models

class BookPublisher(models.Model):
    _name = 'product.book.publisher'
    _description = 'Documentation page'
    _order = 'name DESC'

    name = fields.Char(string='Name')

