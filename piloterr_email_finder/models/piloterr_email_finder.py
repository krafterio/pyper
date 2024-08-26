# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models


class PiloterrEmailFinder(models.Model):
    _name = 'piloterr.email.finder'
    _inherit = ['piloterr.mixin']
    _description = 'Piloterr Email Finder'

    def retrieve_mail(
        self,
        delay: bool,
        header: dict = None,
        callback: str = None,
        model_name: str = None,
        obj_id: int = None,
        field_name: str = None
    ):
        model = self.env[model_name].browse(obj_id)

        company = model.parent_id

        param_url = {
            'query': model.name,
            'company_domain': company.website,
            'company_name': company.name
        }

        self.call_piloterr_request(
            request_type='get',
            delay=delay,
            url=['email', 'finder'],
            header=header,
            param_url=param_url,
            callback=callback,
            model_name=model_name,
            obj_id=obj_id,
            field_name=field_name
        )

    def retrieve_many_mail(
        self,
        delay: bool,
        header: dict = None,
        callback: str = None,
        model_name: str = None,
        obj_id: list = None,
        field_name: str = None
    ):
        for contact in obj_id:
            model = self.env[model_name].browse(contact)
            if not model.is_company:
                company = model.parent_id

                param_url = {
                    'query': model.name,
                    'company_domain': company.website,
                    'company_name': company.name
                }

                self.call_piloterr_request(
                    request_type='get',
                    delay=delay,
                    url=['email', 'finder'],
                    header=header,
                    param_url=param_url,
                    callback=callback,
                    model_name=model_name,
                    obj_id=contact,
                    field_name=field_name
                )

    def set_email(
        self,
        response: str,
        model_name: str,
        obj_id: int,
        field_name: str
    ):
        """
        This function fills the email field of the contact in the given
        object with the response from the request
        :param response: The HTML content returned from the request
        :param model_name: The name of the model where is field_name
        :param obj_id: The object identifier where field_name needs to be updated with the HTML content
        :param field_name: The name of the field in the object where the HTML content should be stored
        """
        obj = self.env[model_name].browse(obj_id)
        setattr(obj, field_name, response['email'])
