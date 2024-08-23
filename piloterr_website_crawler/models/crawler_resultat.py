# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class CrawlerResult(models.Model):
    _name = 'crawler.result'
    _description = 'Crawler Result'

    html_content = fields.Text('HTML Content')
    related_model = fields.Char('Related Model')
    related_id = fields.Integer('Related ID')
