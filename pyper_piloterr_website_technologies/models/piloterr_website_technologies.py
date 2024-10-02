# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import _, models
from odoo.exceptions import UserError


class PiloterrWebsiteTechnologies(models.Model):
    _name = 'piloterr.website.technologies'
    _inherit = ['piloterr.mixin']
    _description = 'Piloterr Website Technologies'

    def add_technologies(
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
            url=['website', 'technology'],
            header=header,
            param_url=param_url,
            callback=callback,
            model_name=model_name,
            obj_id=obj_id,
            field_name='null'
        )


    def add_companies_technologies(
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
                    url=['website', 'technology'],
                    header=header,
                    param_url=param_url,
                    callback=callback,
                    model_name=model_name,
                    obj_id=contact,
                    field_name='null'
                )

    def set_company_technologies(
        self,
        response: str,
        model_name: str,
        obj_id: int,
        field_name: str
    ):
        """
        This function fills the company's contact technologies with the request response
        :param response: The response returned from the request
        :param model_name: The name of the model where add informations
        :param obj_id: The object identifier needs to be updated with the response
        :param field_name: not used but necessary when call set_company_technologies in the request
        """
        obj = self.env[model_name].browse(obj_id)

        for techno in response['technologies']:
            for categorie in techno['categories']:

                res_type = self.env['technology.type'].search([
                    ('name', '=', categorie['name'])
                ])
                if not res_type:
                    res_type = self.env['technology.type'].create({
                        'name': categorie['name']
                    })

                res_techno = self.env['technology'].search([
                    ('name', '=', techno['name']),
                    ('type_id', '=', res_type.id),
                ])
                if res_techno:
                    if obj not in res_techno.partner_ids:
                        res_techno.write({
                            'partner_ids': [(4, obj.id)]
                        })
                else:
                    self.env['technology'].create({
                        'name': techno['name'],
                        'partner_ids': obj,
                        'type_id': res_type.id
                    })
