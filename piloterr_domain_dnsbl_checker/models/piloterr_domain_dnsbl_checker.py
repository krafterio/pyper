# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import _, models
from odoo.exceptions import UserError


class PiloterrDomainDnsblChecker(models.Model):
    _name = 'piloterr.domain.dnsbl.checker'
    _inherit = ['piloterr.mixin']
    _description = 'Piloterr Domain Dnsbl Checker'

    def check_spam(
        self,
        delay: bool,
        header: dict = None,
        callback: str = None,
        model_name: str = None,
        obj_id: int = None,
        field_name: bool = None
    ):
        model = self.env[model_name].browse(obj_id)

        if not model.email:
            raise UserError(_('You have to give a email to complete operation.'))

        domain = model.email.split('@')[-1]

        param_url = {
            'query': domain,
        }

        self.call_piloterr_request(
            request_type='get',
            delay=delay,
            url=['domain', 'dnsbl'],
            header=header,
            param_url=param_url,
            callback=callback,
            model_name=model_name,
            obj_id=obj_id,
            field_name=field_name
        )

    def check_multiple_spam(
        self,
        delay: bool,
        header: dict = None,
        callback: str = None,
        model_name: str = None,
        obj_id: int = None,
        field_name: bool = None
    ):
        for contact in obj_id:
            model = self.env[model_name].browse(contact)

            domain = model.email.split('@')[-1]

            param_url = {
                'query': domain,
            }

            self.call_piloterr_request(
                request_type='get',
                delay=delay,
                url=['domain', 'dnsbl'],
                header=header,
                param_url=param_url,
                callback=callback,
                model_name=model_name,
                obj_id=contact,
                field_name=field_name
            )

    def set_company_technology(
        self,
        response: str,
        model_name: str,
        obj_id: int,
        field_name: bool
    ):
        """
        This function indicates if the contact has an anti-spam configured with the request response
        :param response: The response returned from the request
        :param model_name: The name of the model where add informations
        :param obj_id: The object identifier needs to be updated with the response
        :param field_name: The name of the object field in which anti-spam is used should be stored
        """
        obj = self.env[model_name].browse(obj_id)

        if response['blacklisted'] is True:
            setattr(obj, field_name, True)
        else:
            setattr(obj, field_name, False)
