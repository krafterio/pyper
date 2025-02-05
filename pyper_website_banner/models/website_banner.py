# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import _, fields, models
from datetime import datetime


class WebsiteBanner(models.Model):
    _name = 'website.banner'
    _description = 'Banner header on website'

    name = fields.Char()

    bg_color = fields.Char(string='Background Color', default='#FFFFFF')
    has_second_bg_color = fields.Boolean('Activate second background Color')
    second_bg_color = fields.Char('Second background Color')

    has_outline = fields.Boolean('Has Outline')
    outline_color = fields.Char('Outline Color')
    # height_banner = fields.Integer()

    start_date = fields.Date()
    end_date = fields.Date()

    only_shop = fields.Boolean()
    
    element_ids = fields.Many2many('website.banner.element')
    
    def _get_website_banner(self):
        today = datetime.today().date()

        banner = self.env['website.banner'].search([
            ('start_date', '<=', today),
            ('end_date', '>=', today)
        ], limit=1)
        return banner
