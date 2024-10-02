# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models


class Respartner(models.Model):
    _inherit = 'res.partner'

    def search_piloterr_company(self):
        self.env['piloterr.company.lookup'].retrieve_company_information(
            delay=False,
            callback='set_company_information',
            model_name=self._name,
            obj_id=self.id,
            header={'Content-Type': 'application/json'}
        )

    def search_piloterr_companies(self):
        self.env['piloterr.company.lookup'].retrieve_companies_information(
            delay=True,
            callback='set_company_information',
            model_name=self._name,
            obj_id=self.mapped('id'),
            header={'Content-Type': 'application/json'}
        )
