# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, _
from odoo.exceptions import UserError
import requests

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def action_enrich_company_infos(self):
        for partner in self:
            if not partner.is_company:
                raise UserError(_('You can only enrich company data from a..... company. Right ?'))

            base_url = "https://api.pappers.fr/v2/entreprise"
            api_token = self.env['ir.config_parameter'].sudo().get_param('pyper_pappers_connector.pappers_token_api')

            if not api_token:
                raise UserError(_('You have to complete your pappers token in the settings first.'))
            else:
                url = base_url + "/?api_token=%s" % (api_token)

            r = requests.get(url)

            if r.status_code != 400:
                raise UserError("Invalid API_KEY, please request a valid API KEY on pappers.fr")

            if not partner.siret:
                raise UserError(_('You have to make sure SIRET is filled to complete operation.'))
            else:
                url = base_url + "/?api_token=%s&siret=%s" % (api_token, partner.siret)

            response = requests.get(url)
            company_infos = response.json()

            if response.status_code == 200:
                if company_infos['nom_entreprise']:
                    if company_infos['numero_tva_intracommunautaire']:
                        partner.vat = company_infos['numero_tva_intracommunautaire']

                    if company_infos['code_naf']:
                        partner.ape = company_infos['code_naf']

                    if company_infos['objet_social'] and partner.description is False:
                        partner.description = company_infos['objet_social']

                    if company_infos['date_creation']:
                        partner.creation_date = company_infos['date_creation']

                    if company_infos['etablissement']:
                        if company_infos['etablissement']['adresse_ligne_1']:
                            partner.street = company_infos['etablissement']['adresse_ligne_1'].capitalize()

                        if company_infos['etablissement']['code_postal']:
                            partner.zip = company_infos['etablissement']['code_postal']

                        if company_infos['etablissement']['ville']:
                            partner.city = company_infos['etablissement']['ville'].capitalize()

                        if company_infos['etablissement']['siret']:
                            partner.siret = company_infos['etablissement']['siret']

                        if company_infos['etablissement']['effectif_min']:
                            partner.number_employees_min = company_infos['etablissement']['effectif_min']

                        if company_infos['etablissement']['code_pays']:
                            country_code = company_infos['etablissement']['code_pays']

                            country_id = self.env['res.country'].search(
                                [
                                    ('code', '=', country_code),
                                ],
                            )

                            if country_id.id:
                                partner['country_id'] = country_id.id

                    if company_infos['capital'] and company_infos['devise_capital']:
                        currency_id = self.env['res.currency'].search(
                            [
                                ('currency_unit_label', '=', company_infos['devise_capital']),
                            ],
                        )

                        if currency_id:
                            partner.capital_currency_id = currency_id
                            partner.capital = company_infos['capital']



            elif response.status_code == 400:
                raise UserError(response.json()['message'])

    def search_pappers_company(self):
        for record in self:
            base_url = "https://api.pappers.fr/v2/suggestions"
            url = base_url + "/?q=%s&longueur=50&cibles=nom_entreprise,siret" % (record.name)

            response = requests.get(url)
            companies = response.json()

            if response.status_code == 200:

                companies_info = []

                for company in companies['resultats_nom_entreprise']:
                    companies_info.append((0, 0, {
                        'name': company['nom_entreprise'],
                        'city': company['siege']['ville'],
                        'siret': company['siege']['siret'],
                        'creation_date': company['date_creation'],
                        'zip': company['siege']['code_postal'],
                    }))

                for company in companies['resultats_siret']:
                    companies_info.append((0, 0, {
                        'name': company['nom_entreprise'],
                        'city': company['siege']['ville'],
                        'siret': company['siege']['siret'],
                        'creation_date': company['date_creation'],
                        'zip': company['siege']['code_postal'],
                    }))

                return {
                    'name': _('Update company information'),
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'res_model': 'pappers.name.form',
                    'view_mode': 'form',
                    'target': 'new',
                    'context': {**self.env.context, **{
                        'default_name': record.name,
                        'default_results': companies_info,
                        'default_identified_partner_id': record.id,
                    }},
                }

            elif response.status_code == 400:
                raise UserError(response.json()['message'])
