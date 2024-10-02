# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def retrieve_html_page(self):
        self.env['piloterr.website.crawler'].fetch_html(
            delay=False,
            callback='get_html',
            model_name=self._name,
            obj_id=self.id,
            field_name='null'
        )

    def retrieve_clean_html_page(self):
        self.env['piloterr.website.crawler'].fetch_html(
            delay=False,
            callback='get_clean_html',
            model_name=self._name,
            obj_id=self.id,
            field_name='null'
        )
