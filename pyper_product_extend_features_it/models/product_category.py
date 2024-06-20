# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductCategory(models.Model):
    _inherit = 'product.category'

    product_pattern = fields.Selection(
        [
            ('none', 'None'),
            ('smartphone', 'Smartphone'),
            ('tablet', 'Tablet'),
            ('laptop_computer', 'Laptop computer'),
            ('desktop_computer', 'Desktop Computer'),
        ]
    )