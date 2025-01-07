# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_pattern = fields.Selection(
        related='categ_id.product_pattern',
    )

    operating_system_id = fields.Many2one(
        'product.operating.system',
        'Operating system',
    )

    hard_drive_capacity_id = fields.Many2one(
        'product.storage.capacity',
        'Hard drive capacity',
    )

    hard_drive_type_id = fields.Many2one(
        'product.storage.type',
        'Hard drive type',
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

    screen_quality_id = fields.Many2one(
        'product.screen.quality',
        'Screen quality',
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
    
    height_adjustable = fields.Boolean(
        'Height adjustable',
    )

    rotating = fields.Boolean(
        'Rotating',
    )

    @api.depends('product_variant_ids.product_tmpl_id', 'attribute_line_ids.product_template_value_ids', 'attribute_line_ids')
    def _compute_product_variant_count(self):
        for template in self:
            template.product_variant_count = len(template.attribute_line_ids.product_template_value_ids)
