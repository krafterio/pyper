# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import requests
from odoo import _, api, models
from odoo.exceptions import UserError


class PiloterrCompanyLookup(models.Model):
    _name = 'piloterr.company.lookup'
    _inherit = ['piloterr.mixin']
    _description = 'Piloterr Company Lookup'

    def retrieve_company_information(
        self,
        delay: bool,
        header: dict = None,
        callback: str = None,
        model_name: str = None,
        obj_id: int = None,
    ):
        model = self.env[model_name].browse(obj_id)

        if not model.website:
            raise UserError(_('You have to give a website to complete operation.'))

        param_url = {
            'query': model.website,
        }

        self.call_piloterr_request(
            request_type='get',
            delay=delay,
            url=['company'],
            header=header,
            param_url=param_url,
            callback=callback,
            model_name=model_name,
            obj_id=obj_id,
            field_name='null'
        )

    def retrieve_companies_information(
        self,
        delay: bool,
        header: dict = None,
        callback: str = None,
        model_name: str = None,
        obj_id: int = None,
    ):
        for contact in obj_id:
            model = self.env[model_name].browse(contact)
            if model.is_company:

                param_url = {
                    'query': model.website,
                }

                self.call_piloterr_request(
                    request_type='get',
                    delay=delay,
                    url=['company'],
                    header=header,
                    param_url=param_url,
                    callback=callback,
                    model_name=model_name,
                    obj_id=contact,
                    field_name='null'
                )

    def set_company_information(
        self,
        response: str,
        model_name: str,
        obj_id: int,
        field_name: str
    ):
        """
        This function fills the company contact fields with the response from the request
        :param response: The response returned from the request
        :param model_name: The name of the model where add informations
        :param obj_id: The object identifier needs to be updated with the response
        :param field_name: not used but necessary when call set_company_information in the request
        """
        obj = self.env[model_name].browse(obj_id)

        if response['location']['city'] and not obj.city :
            setattr(obj, 'city', response['location']['city'])

        if response['location']['postcode'] and not obj.zip:
            setattr(obj, 'zip', response['location']['postcode'])

        if response['location']['country_code'] and not obj.country_id:
            country_id = self.env['res.country'].search(
                [
                    ('code', '=', response['location']['country_code']),
                ],
            )
            if country_id.id:
                setattr(obj, 'country_id', country_id.id)

        if response['phone_number'] and not obj.phone:
            setattr(obj, 'phone', response['phone_number'])

        if response['location']['lat'] and not obj.partner_latitude:
            setattr(obj, 'partner_latitude', response['location']['lat'])

        if response['location']['lng'] and not obj.partner_longitude:
            setattr(obj, 'partner_longitude', response['location']['lng'])

        if response['social_networks']['linkedin'] and not obj.company_linkedin:
            setattr(obj, 'company_linkedin', response['social_networks']['linkedin'])

        base_geolocalize_installed = self.env['ir.module.module'].search_count(
            [
                ('name', '=', 'base_geolocalize'),
                ('state', '=', 'installed')
            ]
        ) > 0

        if base_geolocalize_installed and response['location']['lng'] and response['location']['lat']:
            address = self.get_address_from_coordinates(response['location']['lat'], response['location']['lng'])

            street = ''
            if address['address'].get('house_number'):
                street += address['address']['house_number']
            if address['address'].get('road'):
                street += ' ' + address['address']['road']
                setattr(obj, 'street', street)

            if address['address'].get('county'):
                state = self.env['res.country.state'].search(
                    [
                        ('name', '=', address['address']['county']),
                    ],
                )
                if state:
                    setattr(obj, 'state_id', state.id)

            if address['address'].get('postcode'):
                setattr(obj, 'zip', address['address'].get('postcode'))

    @api.model
    def get_address_from_coordinates(self, latitude, longitude):
        url = "https://nominatim.openstreetmap.org/reverse"
        try:
            headers = {'User-Agent': 'Odoo (http://www.odoo.com/contactus)'}
            response = requests.get(url, headers=headers, params={'format': 'json', 'lat': latitude, 'lon': longitude})

        except Exception as e:
            print("Error ", e)

        return response.json()
