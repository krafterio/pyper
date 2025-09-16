# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    linkedin = fields.Char(
        'LinkedIn',
    )

    company_linkedin = fields.Char(
        'Company LinkedIn',
    )

    def import_contact_from_extension(self, data: dict, create_company = False, enrich = False):
        linkedin = data.get('linkedInUrl', False)
        if isinstance(linkedin, str) and self.search(
                [('linkedin', 'ilike', f'{linkedin.rstrip("/")}%')],
                limit=1):
            return

        company = self.env['res.partner']

        if create_company and data.get('companyName'):
            company = company.search([('name', 'ilike', data.get('companyName'))], limit=1, order='name ASC')

            if not company:
                company = company.create({
                    'name': data.get('companyName'),
                    'company_type': 'company',
                })

        records = self.create({
            'name': data.get('fullName', False),
            'image_1920': data.get('avatarData', False),
            'linkedin': linkedin,
            'function': data.get('function', False),
            'comment': data.get('description', False),
            'parent_id': company.id,
        })

        if enrich:
            records._enrich_contact_from_import()

    def import_company_from_extension(self, data: dict, enrich = False):
        linkedin = data.get('linkedInUrl', False)
        if isinstance(linkedin, str) and self.search(
                [('company_linkedin', 'ilike', f'{linkedin.rstrip("/")}%')],
                limit=1):
            return

        records = self.create({
            'name': data.get('name', False),
            'image_1920': data.get('avatarData', False),
            'company_linkedin': linkedin,
            'comment': data.get('description', False),
            'company_type': 'company',
        })

        if enrich:
            records._enrich_company_from_import()

    def _enrich_contact_from_import(self):
        pass

    def _enrich_company_from_import(self):
        pass
