# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_pattern = fields.Selection(
        related='categ_id.product_pattern',
    )

    hard_drive_type = fields.Selection(
        [
            ('HDD', 'HDD'),
            ('SSD', 'SSD'),
        ],
        'Hard drive type',
    )

    operating_system_id = fields.Many2one(
        'product.operating.system',
        'Operating system',
    )

    hard_drive_capacity_id = fields.Many2one(
        'product.storage.capacity',
        'Hard drive capacity',
    )

    ram_capacity_id = fields.Many2one(
        'product.storage.capacity',
        'RAM capacity',
    )

    processor_id = fields.Many2one(
        'product.processor',
        'Processor',
    )

    screen_size_id = fields.Many2one(
        'product.screen.size',
        'Screen size',
    )

    graphic_card_id = fields.Many2one(
        'product.graphic.card',
        'Graphic card',
    )

    has_webcam = fields.Boolean(
        'Has webcam',
    )

    has_bluetooth = fields.Boolean(
        'Has bluetooth',
    )

    has_wifi = fields.Boolean(
        'Has wifi',
    )

    has_optical_drive = fields.Boolean(
        'Has optical drive',
    )
