# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, _, Command, api
from odoo.exceptions import UserError
import requests


class PappersNameForm(models.TransientModel):
    _name = 'pappers.name.form'
    _description = 'Pappers name Form'

    name = fields.Char(
        'Name',
    )

    results = fields.One2many(
        'pappers.name.result.form',
        'name_form',
        'Results',
    )

    identified_partner_id = fields.Many2one(
        'res.partner',
        'Identified partner'
    )

    is_api_key_set = fields.Boolean(
        'API Key set',
        default=False,
    )

    def action_pappers_api_call(self):
        self.ensure_one()

        for record in self:
            base_url = "https://api.pappers.fr/v2/suggestions"

            if not record.name:
                raise UserError(_('You have to give a name to complete operation.'))
            else:
                url = base_url + "/?q=%s&longueur=50&cibles=nom_entreprise,siret" % (record.name)

            response = requests.get(url)
            companies = response.json()

            if response.status_code == 200:

                companies_info = [Command.clear()]

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

                record.results = companies_info

                return {
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'res_model': 'pappers.name.form',
                    'view_mode': 'form',
                    'res_id': record.id,
                    'target': 'new',
                    'context': {**self.env.context, **{
                        'default_name': record.name,
                        'default_results': companies_info,
                    }},
                }


            elif response.status_code == 400:
                raise UserError(response.json()['message'])

    def action_pappers_new_api_call(self):
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'res_model': 'pappers.name.form',
            'view_mode': 'form',
            'target': 'new',
        }

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        res['is_api_key_set'] = bool(self.env['ir.config_parameter'].sudo().get_param('pyper_pappers_connector.pappers_token_api'))
        return res