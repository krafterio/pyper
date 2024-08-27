# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def search_piloterr_technologies(self):
        self.env['piloterr.website.technologies'].add_technologies(
            delay=False,
            callback='set_company_technologies',
            model_name=self._name,
            obj_id=self.id,
        )

    def search_piloterr_companies_technologies(self):
        self.env['piloterr.website.technologies'].add_companies_technologies(
            delay=True,
            callback='set_company_technologies',
            model_name=self._name,
            obj_id=self.mapped('id'),
        )
