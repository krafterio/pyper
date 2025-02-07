# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models


class WebsiteBannerElement(models.Model):
    _name = 'website.banner.element'
    _description = 'Banner header\'s element on website'
    
    sequence = fields.Integer()
    
    type = fields.Selection([
        ('text', 'Text'),
        ('link', 'Link'),
        ('product', 'Product'),
        ('page', 'Page'),
    ])

    content = fields.Char()
    
    is_btn = fields.Boolean('Button style')
    text_color = fields.Char('Text')
    bg_color = fields.Char('Background')
    outline_color = fields.Char('Border')
    is_bold = fields.Boolean('Bold')
    is_italic = fields.Boolean('Italic')

    link = fields.Char()
    product_tmpl_id = fields.Many2one('product.template', 'Product')
    page_id = fields.Many2one('website.page', 'Page')
    
    def action_remove_color_bg(self):
        self.bg_color = False
        
    def action_remove_color_text(self):
        self.text_color = False
        
    def action_remove_color_outline(self):
        self.outline_color = False