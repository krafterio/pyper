# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    linkedin_url = fields.Char(
        'Linkedin url'
    )

    company_linkedin_url = fields.Char(
        'Company LinkedIn Url',
    )

    def import_contact_from_extension(self, data: dict, create_company = False, enrich = False):
        linkedin_url = data.get('linkedInUrl', False)
        if isinstance(linkedin_url, str) and self.search(
                [('linkedin_url', 'ilike', f'{linkedin_url.rstrip("/")}%')],
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
            'linkedin_url': linkedin_url,
            'function': data.get('function', False),
            'comment': data.get('description', False),
            'parent_id': company.id,
        })

        if enrich:
            records._enrich_contact_from_import()

    def import_company_from_extension(self, data: dict, enrich = False):
        linkedin_url = data.get('linkedInUrl', False)
        if isinstance(linkedin_url, str) and self.search(
                [('company_linkedin_url', 'ilike', f'{linkedin_url.rstrip("/")}%')],
                limit=1):
            return

        records = self.create({
            'name': data.get('name', False),
            'image_1920': data.get('avatarData', False),
            'company_linkedin_url': linkedin_url,
            'comment': data.get('description', False),
            'company_type': 'company',
        })

        if enrich:
            records._enrich_company_from_import()

    def _enrich_contact_from_import(self):
        pass

    def _enrich_company_from_import(self):
        pass
