# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, _
from odoo.exceptions import UserError
import requests
import urllib.parse

class PappersNameResultForm(models.TransientModel):
    _name = 'pappers.name.result.form'
    _description = 'Pappers name result Form'

    name = fields.Char(
        'Name',
    )

    siret = fields.Char(
        'Siret',
    )

    city = fields.Char(
        'city',
    )

    creation_date = fields.Date(
        'Creation date',
    )

    zip = fields.Char(
        'Zip code',
    )

    name_form = fields.Many2one(
        'pappers.name.form',
        'Name form',
    )

    identified_partner_id = fields.Many2one(
        related="name_form.identified_partner_id"
    )

    result_json = fields.Json()

    def action_create_company_siret(self):
        self.ensure_one()

        for record in self:
            base_url = "https://api.pappers.fr/v2/suggestions"
            name = urllib.parse.quote(record.siret, safe='')

            url = base_url + "/?q=%s&longueur=80&cibles=nom_entreprise,siret" % (name)

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

    def action_update_company_pappers(self):
        siret = self.env.context.get('pappers_siret')
        identified_partner = self.env.context.get('pappers_identified_partner')

        partner_id = self.env['res.partner'].search([('id', '=', identified_partner)])
        partner_id.siret = siret

        partner_id.action_enrich_company_infos(self.env.context.get('result_json'))
