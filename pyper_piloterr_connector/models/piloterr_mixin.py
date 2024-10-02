# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import logging

import requests
from odoo import _, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

TIMEOUT = 60


class PiloterrMixin(models.AbstractModel):
    _name = 'piloterr.mixin'
    _description = 'Piloterr Mixin'

    def call_piloterr_request(
        self,
        request_type: str,
        delay: bool,
        url: list,
        data: dict = None,
        header: dict = None,
        param_url: list = None,
        callback: str = None,
        model_name: str = None,
        obj_id: int = None,
        field_name: str = None
    ):
        """
        This function sends a request to the Piloterr v2 API with the specified request type and the given parameters

        :param request_type: The type of request (GET or POST)
        :param delay: Indicates whether the request has a time limit
        :param url: List of URL segments to be added after 'https://piloterr.com/api/v2/'
            to form the complete request URL
        :param data: Data to be sent in the body of the POST request in JSON format
        :param header: Dictionary of additional headers to include in the HTTP request
        :param param_url: Additional parameters to include in the URL's query string
        :param callback: The name of the function to be called after the request
            to process the result
        :param model_name: The name of the model where is field_name
        :param obj_id: The object identifier where field_name needs to be updated
            with the query response
        :param field_name: The name of the field where to put the query response

        :raises UserError: If the request type is not 'GET' or 'POST'
        """

        if request_type.upper() == 'GET':
            self._piloterr_get_request(
                url=url,
                delay=delay,
                header=header,
                param_url=param_url,
                callback=callback,
                model_name=model_name,
                obj_id=obj_id,
                field_name=field_name
            )
        elif request_type.upper() == 'POST':
            self._piloterr_post_request(
                url=url,
                delay=delay,
                data=data,
                callback=callback,
                model_name=model_name,
                obj_id=obj_id,
                field_name=field_name
            )
        else:
            raise UserError(f'The request type {request_type} doesn\'t exist')

    def _piloterr_get_request(
        self,
        url,
        delay,
        header=None,
        param_url=None,
        callback=None,
        model_name=None,
        obj_id=None,
        field_name=None
    ):
        if delay:
            self.with_delay(auto_unlink='none')._execute_get_request(
                url=url,
                header=header,
                param_url=param_url,
                callback=callback,
                model_name=model_name,
                obj_id=obj_id,
                field_name=field_name
            )
        else:
            self._execute_get_request(
                url=url,
                header=header,
                param_url=param_url,
                callback=callback,
                model_name=model_name,
                obj_id=obj_id,
                field_name=field_name
            )

    def _piloterr_post_request(
        self,
        url,
        delay,
        data,
        callback=None,
        model_name=None,
        obj_id=None,
        field_name=None
    ):
        if delay:
            self.with_delay(auto_unlink='none')._execute_post_request(
                url=url,
                data=data,
                callback=callback,
                model_name=model_name,
                obj_id=obj_id,
                field_name=field_name
            )
        else:
            self._execute_post_request(
                url=url,
                data=data,
                callback=callback,
                model_name=model_name,
                obj_id=obj_id,
                field_name=field_name
            )

    def _execute_get_request(
        self,
        url: list,
        header: dict = None,
        param_url: list = None,
        callback: str = None,
        model_name: str = None,
        obj_id: int = None,
        field_name: str = None
    ):
        """
        This function sends a GET request to the Piloterr v2 API with the given parameters

        :param url: List of URL segments to be added after 'https://piloterr.com/api/v2/'
            to form the complete request URL
        :param header: Dictionary of additional headers to include in the HTTP request
        :param param_url: Additional parameters to include in the URL's query string
        :param callback: The name of the function to be called after the request
            to process the result
        :param model_name: The name of the model where is field_name
        :param obj_id: The object identifier where field_name needs to be updated
            with the query response
        :param field_name: The name of the field where to put the query response

        :raise UserError: If the API token is missing or if an HTTP/Request error
            occurs.

        Notes:
        - HTTP error codes are specifically handled to provide insight into the
            issue (e.g., invalid API token, parameter errors, billing issues).
        - Errors are logged for diagnostic and debugging purposes.
        """

        api_token = self.env['ir.config_parameter'].sudo().get_param('pyper_piloterr_connector.piloterr_token_api')

        if not api_token:
            raise UserError(_('You have to complete your Piloterr token in the settings first.'))

        if url:
            url = 'https://piloterr.com/api/v2/' + '/'.join(url)

        if param_url:
            query_params = []
            for key, value in param_url.items():
                query_params.append(f'{key}={value}')
            url = url + '?' + '&'.join(query_params)

        headers = {'x-api-key': api_token}
        if header:
            headers.update(header)

        try:
            response = requests.get(url, headers=headers, timeout=TIMEOUT)
            response.raise_for_status()

            method = getattr(self, callback, None)
            if callback and method:
                if model_name and field_name and obj_id:
                    method(response=response.json(), obj_id=obj_id, model_name=model_name, field_name=field_name)
                else:
                    method(response.json())
            else:
                raise UserError(
                    _("The callback method '%(callback)s' does not exist in the model '%(model)s'.",
                        callback=callback,
                        model=self._name)
                )
        except requests.exceptions.HTTPError as http_err:
            # See 400, 401, 402, 403, 404, 500 errors
            if response.status_code == 400:
                message = (f"""HTTP Error: {http_err}
                            Verify your parameters and their types.
                            Ensure your API key is active and not expired.""")
            elif response.status_code == 401:
                message = (f"""HTTP Error: {http_err}
                            Check your API key and ensure it is valid.""")
            elif response.status_code == 402:
                message = (f"""HTTP Error: {http_err}
                            Settle any outstanding invoices to continue using the API.""")
            elif response.status_code == 403:
                message = (f"""HTTP Error: {http_err}
                            Verify your permissions.
                            Contact us if you believe this is a mistake.""")
            elif response.status_code == 404:
                message = (f"""HTTP Error: {http_err}
                            Ensure the endpoint URL is correct.
                            This is billed except for specific endpoints listed below.
                            /api/v2/company
                            /api/v2/company/suggest
                            /api/v2/company/social
                            /api/v2/linkedin/company/info""")
            elif response.status_code == 500:
                message = (f"""HTTP Error: {http_err}
                            Retry the action and check the detailed error message in the response body
                            for more insights.""")
            else:
                message = (f'HTTP Error: {http_err}')
            _logger.error(message)
            raise UserError(message)
        except requests.exceptions.RequestException as req_err:
            _logger.error(f'Request error occurred: {req_err}')
            raise UserError(f'Request error occurred: {req_err}')

    def _execute_post_request(
        self,
        url: list,
        data: dict = None,
        callback: str = None,
        model_name: str = None,
        obj_id: int = None,
        field_name: str = None,
    ):
        """
        This function sends a POST request to the Piloterr v2 API  with the given parameters

        :param url: List of URL segments to be added after 'https://piloterr.com/api/v2/'
            to form the complete request URL
        :param data: Data to be sent in the body of the POST request in JSON format
        :param callback: The name of the function to be called after the request
            to process the result
        :param model_name: The name of the model where is field_name
        :param obj_id: The object identifier where field_name needs to be updated
            with the query response
        :param field_name: The name of the field where to put the query response

        :raise UserError: If the API token is missing or if an HTTP/Request error
            occurs.

        Notes:
        - HTTP error codes are specifically handled to provide insight into the
            issue (e.g., invalid API token, parameter errors, billing issues).
        - Errors are logged for diagnostic and debugging purposes.
        """

        api_token = self.env['ir.config_parameter'].sudo().get_param('pyper_piloterr_connector.piloterr_token_api')

        if not api_token:
            raise UserError(_('You have to complete your Piloterr token in the settings first.'))

        if url:
            url = 'https://piloterr.com/api/v2/' + '/'.join(url)

        headers = {
            'x-api-key': api_token,
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, headers=headers, json=data, timeout=TIMEOUT)
            response.raise_for_status()

            method = getattr(self, callback, None)
            if callback and method:
                if model_name and field_name and obj_id:
                    method(response=response.json(), obj_id=obj_id, model_name=model_name, field_name=field_name)
                else:
                    method(response.json())
            else:
                raise UserError(
                    _("The callback method '%(callback)s' does not exist in the model '%(model)s'.",
                        callback=callback,
                        model=self._name)
                )
        except requests.exceptions.HTTPError as http_err:
            # See 400, 401, 402, 403, 404, 500 errors
            if response.status_code == 400:
                message = (f"""HTTP Error: {http_err}
                            Verify your parameters and their types.
                            Ensure your API key is active and not expired.""")
            elif response.status_code == 401:
                message = (f"""HTTP Error: {http_err}
                            Check your API key and ensure it is valid.""")
            elif response.status_code == 402:
                message = (f"""HTTP Error: {http_err}
                            Settle any outstanding invoices to continue using the API.""")
            elif response.status_code == 403:
                message = (f"""HTTP Error: {http_err}
                            Verify your permissions.
                            Contact us if you believe this is a mistake.""")
            elif response.status_code == 404:
                message = (f"""HTTP Error: {http_err}
                            Ensure the endpoint URL is correct.
                            This is billed except for specific endpoints listed below.
                            /api/v2/company
                            /api/v2/company/suggest
                            /api/v2/company/social
                            /api/v2/linkedin/company/info""")
            elif response.status_code == 500:
                message = (f"""HTTP Error: {http_err}
                            Retry the action and check the detailed error message in the response body
                            for more insights.""")
            else:
                message = (f'HTTP Error: {http_err}')
            _logger.error(message)
            raise UserError(message)
        except requests.exceptions.RequestException as req_err:
            _logger.error(f'Request error occurred: {req_err}')
            raise UserError(f'Request error occurred: {req_err}')
