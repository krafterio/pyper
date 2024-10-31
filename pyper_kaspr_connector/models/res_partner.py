# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, _
from datetime import datetime
from datetime import timedelta

from odoo.exceptions import UserError
import requests


class ResPartner(models.Model):
    _inherit = 'res.partner'

    linkedin_id = fields.Char(
        'Linkedin id',
    )

    def action_open_kaspr_form(self):
        wizard_id = self.env['kaspr.form'].create([])

        return {
            'name': _('Get linkedin info'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'kaspr.form',
            'res_id': wizard_id.id
        }

    def action_update_kaspr_linkedin_email_form(self):
        self.action_update_kaspr_linkedin_form(
            ["workEmail"],
        )

    def action_update_kaspr_linkedin_phone_form(self):
        self.action_update_kaspr_linkedin_form(
            [
                "phone",
                "workEmail"
            ],
        )

    def action_update_kaspr_linkedin_form(self):
        for contact in self:
            if contact.is_company:
                raise UserError(_('You can only enrich contact data from a..... contact. Right ?'))

            if not contact.linkedin_url:
                raise UserError(_('You have to fill linkedin url on contact profil.'))

            if 'linkedin.com/in/' not in contact.linkedin_url:
                raise UserError(_('Not a linkedin URL. Please paste full linkedin URL'))
            api_token = self.env['ir.config_parameter'].sudo().get_param('pyper_kaspr_connector.kaspr_token_api')

            if not api_token:
                raise UserError(_('You have to fill the Kaspr token API in the global settings first.'))

            linkedin_id = contact.linkedin_url.split("linkedin.com/in/")[1].replace('/', '')

            url = "https://api.developers.kaspr.io/profile/linkedin"

            payload = {
                "id": linkedin_id,
                "name": contact.name,
                "dataToGet": ["phone","workEmail"]
            }

            headers = {
                "Prefer": "code=200",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "accept-version": "v2.0",
                "authorization": "Bearer " + api_token,
            }
            try:
                response = requests.post(url, json=payload, headers=headers)
                response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
                contact_infos = response.json()

                if not contact_infos:
                    raise UserError(_('No data found for this contact'))
    
                if contact.email is False:
                    if contact_infos['profile']['starryWorkEmail']:
                        contact.email = contact_infos['profile']['starryWorkEmail']
                    elif contact_infos['profile']['workEmails']:
                        contact.email = contact_infos['profile']['workEmails']
                    elif contact_infos['profile']['professionalEmails']:
                        contact.email = contact_infos['profile']['professionalEmails'][0]

                if contact_infos['profile']['starryPhone'] and not contact.mobile:
                    contact.mobile = contact_infos['profile']['starryPhone']

            except requests.exceptions.HTTPError as http_err:
                if response.status_code == 401:
                    raise UserError(_('Invalid API token. Please check your Kaspr API token in the global settings.'))
                else:
                    raise UserError(_('HTTP error occurred: %s') % http_err)
            except requests.exceptions.RequestException as req_err:
                raise UserError(_('Request error occurred: %s') % req_err)


