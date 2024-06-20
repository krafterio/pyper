# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, api, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_book = fields.Boolean(
        'Is book',
        related="categ_id.is_book",
    )

    publisher_id = fields.Many2one(
        'product.book.publisher',
        'Publisher',
    )

    isbn13 = fields.Char(
        'ISBN 13',
        size=13,
    )

    authors = fields.Char(
        'Authors',
    )

    date_published = fields.Date(
        'Date Published',
    )

    pages = fields.Integer(
        'Pages',
    )

    language_id = fields.Many2one(
        'res.lang',
        'Language',
    )
