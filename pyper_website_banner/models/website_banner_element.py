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
    bg_color = fields.Char('Background')

    link = fields.Char()
    product_tmpl_id = fields.Many2one('product.template', 'Product')
    page_id = fields.Many2one('website.page', 'Page')
    
    def action_remove_color_bg(self):
        self.bg_color = False
        
    def action_remove_color_text(self):
        self.text_color = False
        
    def action_remove_color_outline(self):
        self.outline_color = False
        
    @api.onchange('type')
    def _onchange_elements_type(self):
        if self.type != 'link':
            self.link = False
        if self.type != 'product':
            self.product_tmpl_id = False
        if self.type != 'page':
            self.page_id = False
