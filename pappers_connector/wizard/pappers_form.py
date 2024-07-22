# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
from types import NoneType

from odoo import fields, models, _
from odoo.exceptions import UserError
import requests

class PappersForm(models.TransientModel):
    _name = 'pappers.form'
    _description = 'Pappers Form'

    siret = fields.Char(
        'Siret',
        size=14,
    )

    def action_pappers_api_call(self):
        self.ensure_one()

        for record in self:
            base_url = "https://api.pappers.fr/v2/suggestions"

            url = base_url + "/?q=%s&longueur=80&cibles=nom_entreprise,siret" % record.siret

            response = requests.get(url)
            companies = response.json()

            company = companies['resultats_siret'][0]

            if response.status_code == 200:
                partner_obj = self.env['res.partner']

                if company['nom_entreprise']:
                    company_name = company['nom_entreprise'].title()

                    partners = partner_obj.search([('name', '=', company_name)], limit=1)

                    if len(partners) > 0:
                        partner = partners[0]
                    else:
                        partner = self.env['res.partner'].create({
                            'name': company['nom_entreprise'].title(),
                            'is_company': True,
                        })

                    if company['code_naf']:
                        partner.ape = company['code_naf']

                    if company['date_creation']:
                        partner.creation_date = company['date_creation']

                    if company['siege']:
                        if company['siege']['adresse_ligne_1']:
                            partner.street = company['siege']['adresse_ligne_1'].capitalize()

                        if company['siege']['code_postal']:
                            partner.zip = company['siege']['code_postal']

                        if company['siege']['ville']:
                            partner.city = company['siege']['ville'].capitalize()

                        if company['siege']['siret']:
                            partner.siret = company['siege']['siret']

                        if company['effectifs_finances']:
                            partner.number_employees_min = company['effectifs_finances']

                        country_id = self.env['res.country'].search(
                            [
                                ('code', '=', 'FR'),
                            ],
                        )

                        if country_id.id:
                            partner['country_id'] = country_id.id

                    if company['capital']:
                        currency_id = self.env['res.currency'].search(
                            [
                                ('name', '=', 'EUR'),
                            ],
                        )

                        if currency_id:
                            partner.capital_currency_id = currency_id
                            partner.capital = company['capital']

                    if company['resultat']:
                        partner.revenue = company['resultat']

                    if company['annee_finances']:
                        partner.financial_data_year = company['annee_finances']

                    if partner:
                        return {
                            'type': 'ir.actions.act_window',
                            'view_type': 'form',
                            'res_model': 'res.partner',
                            'view_mode': 'form',
                            'res_id': partner.id,
                            'target': 'current',
                        }
            elif response.status_code == 400:
                raise UserError(response.json()['message'])

