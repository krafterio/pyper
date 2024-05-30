# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_manufacturer_id = fields.Many2one(
        'product.manufacturer',
        'Manufacturer',
    )
