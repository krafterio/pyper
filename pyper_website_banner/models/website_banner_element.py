# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import _, fields, models
from datetime import datetime


class WebsiteBannerElement(models.Model):
    _name = 'website.banner.element'
    _description = 'Banner header\'s element on website'
    
    content = fields.Char()
    text_color = fields.Char()

    link = fields.Char()
    
    is_btn = fields.Boolean('Button style')
    bg_color = fields.Char('Background color')
    outline_color = fields.Char('Border color')
    is_bold = fields.Boolean('Bold')
    
    product_tmpl_id = fields.Many2one('product.template', 'Product')
    page_id = fields.Many2one('website.page', 'Page')
