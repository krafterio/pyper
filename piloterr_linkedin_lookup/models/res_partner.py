# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models, _
from odoo.exceptions import UserError
import requests
import base64


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def action_search_piloterr_linkedin_profil(self):
        self.with_delay().search_piloterr_linkedin_profil()

    def search_piloterr_linkedin_profil(self):
        for contact in self:
            if contact.is_company:
                raise UserError(_('You can only enrich contact data from a..... contact. Right ?'))

            api_token = self.env['ir.config_parameter'].sudo().get_param('piloterr_connector.piloterr_token_api')

            if not api_token:
                raise UserError(_('You have to complete your Piloterr token in the settings first.'))

            url = "https://piloterr.com/api/v2/linkedin/profile/info?query="
            url_with_contact = url + contact.linkedin_url

            headers = {"x-api-key": api_token}
            try:
                response = requests.get(url_with_contact, headers=headers)
                response.raise_for_status()
                linkedin_info = response.json()

                if linkedin_info['photo_url']:
                    contact.image_1920 = base64.b64encode(requests.get(linkedin_info['photo_url']).content)

                if linkedin_info['headline']:
                    contact.function = linkedin_info['headline']

                if linkedin_info['full_name']:
                    contact.name = linkedin_info['full_name']

                if len(linkedin_info['experiences']) > 0 and not contact.parent_id.company_linkedin_url:
                    contact.parent_id.company_linkedin_url = linkedin_info['experiences'][0]['company_url']

            except requests.exceptions.HTTPError as http_err:
                # See 404, 500, etc. errors
                # print(f"HTTP error occurred: {http_err}")
                pass
            except requests.exceptions.RequestException as req_err:
                print(f"Request error occurred: {req_err}")

    def action_search_piloterr_linkedin_company_profil(self):
        self.with_delay().search_piloterr_linkedin_company_profil()

    def search_piloterr_linkedin_company_profil(self):
        for partner in self:
            if not partner.is_company:
                raise UserError(_('You can only enrich company data from a..... company. Right ?'))

            api_token = self.env['ir.config_parameter'].sudo().get_param('piloterr_connector.piloterr_token_api')

            if not api_token:
                raise UserError(_('You have to complete your Piloterr token in the settings first.'))

            url = "https://piloterr.com/api/v2/linkedin/company/info?query="
            url_with_contact = url + partner.company_linkedin_url

            headers = {"x-api-key": api_token}
            try:
                response = requests.get(url_with_contact, headers=headers)
                response.raise_for_status()
                linkedin_info = response.json()

                if linkedin_info['logo_url']:
                    partner.image_1920 = base64.b64encode(requests.get(linkedin_info['logo_url']).content)

                for partner in self:
                    if not partner.is_company:
                        raise UserError(_('You can only enrich company data from a..... company. Right ?'))

                    api_token = self.env['ir.config_parameter'].sudo().get_param(
                        'piloterr_connector.piloterr_token_api')

                    if not api_token:
                        raise UserError(_('You have to complete your Piloterr token in the settings first.'))

                    url = "https://piloterr.com/api/v2/linkedin/company/info?query="
                    url_with_contact = url + partner.company_linkedin_url

                    headers = {"x-api-key": api_token}
                    try:
                        response = requests.get(url_with_contact, headers=headers)
                        response.raise_for_status()
                        linkedin_info = response.json()

                        if linkedin_info['logo_url']:
                            partner.image_1920 = base64.b64encode(requests.get(linkedin_info['logo_url']).content)

                        if linkedin_info['website']:
                            partner.website = linkedin_info['website']

                        if linkedin_info['description'] and not partner.comment:
                            partner.comment = linkedin_info['description']

                        if linkedin_info['staff_count']:
                            partner.number_employees_min = linkedin_info['staff_count']

                    except requests.exceptions.HTTPError as http_err:
                        # See 404, 500, etc. errors
                        # print(f"HTTP error occurred: {http_err}")
                        pass
                    except requests.exceptions.RequestException as req_err:
                        print(f"Request error occurred: {req_err}")
                if linkedin_info['website']:
                    partner.website = linkedin_info['website']

                if linkedin_info['description'] and not partner.comment:
                    partner.comment = linkedin_info['description']

                if linkedin_info['staff_count']:
                    partner.number_employees_min = linkedin_info['staff_count']

            except requests.exceptions.HTTPError as http_err:
                # See 404, 500, etc. errors
                # print(f"HTTP error occurred: {http_err}")
                pass
            except requests.exceptions.RequestException as req_err:
                print(f"Request error occurred: {req_err}")
