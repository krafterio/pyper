# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).
from types import NoneType

from odoo import fields, models, _
from odoo.exceptions import UserError
import requests
import json


class KasprForm(models.TransientModel):
    _name = 'kaspr.form'
    _description = 'Kaspr Form'

    linkedin_url = fields.Char(
        'Linkedin URL'
    )

    linkedin_name = fields.Char(
        'Linkedin name',
    )

    company_id = fields.Many2one(
        'res.partner',
        'Company',
        domain=[('is_company', '=', True)],
        help='Leave empty if you want to create company with contact automatically.'
    )

    def action_kaspr_form(self):
        self.ensure_one()

        for record in self:
            if not record.linkedin_url or not record.linkedin_name:
                raise UserError(_('You have to fill linkedin url and name.'))

            if 'linkedin.com/in/' not in record.linkedin_url:
                raise UserError(_('Not a linkedin URL. Please paste full linkedin URL'))
            else:

                api_token = self.env['ir.config_parameter'].sudo().get_param('pyper_kaspr_connector.kaspr_token_api')

                if not api_token:
                    raise UserError(_('You have to fill the Kaspr token API in the global settings first.'))

                linkedin_id = record.linkedin_url.split("linkedin.com/in/")[1].replace('/', '')

                url = "https://api.developers.kaspr.io/profile/linkedin"

                payload = {
                    "id": linkedin_id,
                    "name": record.linkedin_name,
                    "dataToGet": ["workEmail"]
                }

                headers = {
                    "Prefer": "code=200",
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "accept-version": "v2.0",
                    "authorization": "Bearer " + api_token,
                }

                response = requests.post(url, json=payload, headers=headers)
                contact_infos = response.json()

                if response.status_code == 500:
                    raise UserError(contact_infos['message'])

                new_contact = {
                    'type': 'contact',
                    'linkedin_url': record.linkedin_url,
                }

                if bool(contact_infos) is False:
                    raise UserError(_('No infos found for this contact.'))

                try:
                    new_contact['name'] = contact_infos['profile']['name'].title()
                except KeyError:
                    pass

                try:
                    if contact_infos['profile']['starryWorkEmail']:
                        new_contact['email'] = contact_infos['profile']['starryWorkEmail']
                    elif contact_infos['profile']['workEmails']:
                        new_contact['email'] = contact_infos['profile']['workEmails']
                    else:
                        new_contact['email'] = contact_infos['profile']['professionalEmails'][0]
                except KeyError:
                    pass

                try:
                    new_contact['city'] = contact_infos['profile']['location']
                except KeyError:
                    pass

                try:
                    new_contact['function'] = contact_infos['profile']['title']
                except KeyError:
                    pass

                try:
                    new_contact['linkedin_id'] = contact_infos['profile']['id']
                except KeyError:
                    pass

                try:
                    new_contact['phone'] = contact_infos['profile']['starryPhone']
                except KeyError:
                    pass

                try:
                    if record.company_id:
                        new_contact['parent_id'] = record.company_id.id

                    elif contact_infos['profile']['company'] and contact_infos['profile']['company']['name']:
                        company_id = self.env['res.partner'].search(
                            [
                                ('name', '=', contact_infos['profile']['company']['name']),
                            ],
                            limit=1,
                        ).id

                        if company_id is not False:
                            new_contact['parent_id'] = company_id
                        else:
                            new_company = self.env['res.partner'].create({
                                'name': contact_infos['profile']['company']['name'],
                                'is_company': True,
                                'type': 'contact',
                            })

                            new_contact['parent_id'] = new_company.id

                            try:
                                new_company['city'] = contact_infos['profile']['company']['addresses'][0]['city']
                            except KeyError:
                                pass

                            try:
                                new_company['website'] = contact_infos['profile']['company']['companyPageUrl']
                            except KeyError:
                                pass

                            try:
                                new_company['street'] = contact_infos['profile']['company']['addresses'][0]['line1']
                            except KeyError:
                                pass

                            try:
                                new_company['zip'] = contact_infos['profile']['company']['addresses'][0]['postalCode']
                            except KeyError:
                                pass

                            try:
                                new_company['description'] = contact_infos['profile']['company']['description']
                            except KeyError:
                                pass

                            try:
                                new_company['website'] = contact_infos['profile']['company']['companyPageUrl']
                            except KeyError:
                                pass

                            try:
                                if contact_infos['profile']['company']['addresses'][0]['country']:
                                    country_code = contact_infos['profile']['company']['addresses'][0]['country']

                                    country_id = self.env['res.country'].search(
                                        [
                                            ('code', '=', country_code),
                                        ],
                                    )

                                    if country_id.id:
                                        new_company['country_id'] = country_id.id

                            except KeyError:
                                pass

                except KeyError:
                    pass

                new_contact = self.env['res.partner'].create(new_contact)

                return {
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'res_model': 'res.partner',
                    'view_mode': 'form',
                    'res_id': new_contact.id,
                    'target': 'current',
                }
