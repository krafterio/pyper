# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.model_create_multi
    def create(self, vals_list):
        companies = super().create(vals_list)

        self._create_organization(companies)

        return companies

    def _create_organization(self, companies):
        self.env['organization'].sudo().create([{
            'name': company.name,
            'company_id': company.id,
            'image_1920': company.logo,
        } for company in companies])
