# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, _, fields, models
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

    padding = fields.Integer()

    activate_mode = fields.Selection([
        ('date', 'Date'),
        ('manually', 'Manually'),
    ])
    start_date = fields.Date()
    end_date = fields.Date()
    activate = fields.Boolean()

    only_shop = fields.Boolean()
    
    element_ids = fields.Many2many('website.banner.element')
    
    def _get_website_banner(self):
        today = datetime.today().date()

        banner = self.env['website.banner'].search([
            ('activate_mode', '=', 'date'),
            ('start_date', '<=', today),
            ('end_date', '>=', today),
        ], order='start_date asc, end_date asc', limit=1)
        if not banner:
            banner = self.env['website.banner'].search([
                ('activate_mode', '=', 'manually'),
                ('activate', '=', True)
            ], limit=1)

        return banner

    @api.onchange('activate_mode')
    def _onchange_activate_mode(self):
        if self.activate_mode != 'manually':
            self.activate = False
        elif self.activate_mode != 'date':
            self.start_date = False
            self.end_date = False
