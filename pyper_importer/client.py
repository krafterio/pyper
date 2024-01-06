# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from abc import ABC

from requests import Response, request
from requests.auth import AuthBase

from odoo import api, _

from .exceptions import (
    PyperImporterError,
    PyperImporterException,
    PyperImporterHttpError,
    PyperImporterAuthenticationError,
    PyperImporterAuthorizationError,
    PyperImporterConfigurationError,
    PyperImporterJSONDecodeError,
)


def _get_json_data(response: Response, raise_error: bool = True) -> dict:
    try:
        res_data = response.json()
    except ValueError as err:
        res_data = {}

        if raise_error:
            raise PyperImporterJSONDecodeError(str(err))

    return res_data


class ClientHttpResponse:
    def __init__(self, response: Response, data: dict):
        self.response = response
        self.ok = response.ok
        self.status_code = response.status_code
        self.data = data


class BaseHttpClient(ABC):
    def __init__(self,
                 env: api.Environment,
                 base_url: str,
                 auth: AuthBase | None = None,
                 lang: str | None = None,
                 timezone: str | None = None,
                 limit: int | None = None,
                 timeout: int | None = None,
                 disable_ssl_verify: bool | None = None,
                 ):
        IrConfigParameter = env['ir.config_parameter'].sudo()

        self.base_url = base_url
        self.auth = auth
        self.lang = env.user.lang if lang is None else lang
        self.timezone = timezone
        self.limit = limit
        self.timeout = timeout
        self.disable_ssl_verify = disable_ssl_verify

        if self.limit is None:
            self.limit = int(IrConfigParameter.get_param('pyper_importer.http_client.limit', 100))

        if self.timeout is None:
            self.timeout = int(IrConfigParameter.get_param('pyper_importer.http_client.timeout', 60))

    @property
    def _error_message_data_field(self):
        return 'message'

    def base_request(self,
                     method: str,
                     path: str,
                     values: dict | None = None,
                     **kwargs
                     ) -> ClientHttpResponse:
        """Constructs and sends a :class:`Request <Request>`.

        :param method: method for the new :class:`Request` object: ``GET``, ``OPTIONS``, ``HEAD``, ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
        :param path: Path for the new :class:`Request` object without the base URL.
        :param values: (optional) Define the json request body for POST or UPDATE methods.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
        :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
        :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
        :param files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
            ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
            or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string
            defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
            to add for the file.
        :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
        :param timeout: (optional) How many seconds to wait for the server to send data
            before giving up, as a float, or a :ref:`(connect timeout, read
            timeout) <timeouts>` tuple.
        :type timeout: float or tuple
        :param allow_redirects: (optional) Boolean. Enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection. Defaults to ``True``.
        :type allow_redirects: bool
        :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
        :param verify: (optional) Either a boolean, in which case it controls whether we verify
                the server's TLS certificate, or a string, in which case it must be a path
                to a CA bundle to use. Defaults to ``True``.
        :param stream: (optional) if ``False``, the response content will be immediately downloaded.
        :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
        :return: :class:`Response <Response>` object
        :rtype: Response
        """
        kwargs = self.prepare_kwargs_request(**kwargs)

        if values:
            kwargs['json'] = values

        if '://' in path or path.startswith('//'):
            url = path
        else:
            url = (self.base_url.strip('/') + '/' + path.strip('/')).strip('/')

        if 'Accept-Language' not in kwargs['headers']:
            kwargs['headers'].update({'Accept-Language': self.lang})

        if 'Accept' not in kwargs['headers']:
            kwargs['headers'].update({'Accept': 'application/json'})

        if 'Content-type' not in kwargs['headers']:
            kwargs['headers'].update({'Content-type': 'application/json'})

        if 'timeout' not in kwargs:
            kwargs.update({'timeout': self.timeout})

        if 'disable_ssl_verify' not in kwargs:
            kwargs['verify'] = not self.disable_ssl_verify

        if 'auth' not in kwargs and self.auth is not None:
            kwargs.update({'auth': self.auth})

        if 'auth' not in kwargs:
            raise PyperImporterConfigurationError(_('Authentication must be configured in Parameters'))

        try:
            response = request(method, url=url, **kwargs)
            status_code = response.status_code
            res_data = _get_json_data(response, False)
            mess_field = self._error_message_data_field

            if status_code == 401:
                raise PyperImporterAuthenticationError(res_data.get(mess_field) if mess_field in res_data else _(
                    'The Authentication configuration is invalid'))

            if status_code == 403:
                raise PyperImporterAuthorizationError(res_data.get(mess_field) if mess_field in res_data else _(
                    'The Authentication configuration does not have the authorization'))

            if status_code >= 300:
                msg = _("Status code: {} \n Reason: {}").format(status_code, response.reason)

                if mess_field in res_data:
                    msg = msg + "\n" + _("Error message:\n\n{}").format(res_data.get(mess_field))

                raise PyperImporterHttpError(status_code, msg)

            return ClientHttpResponse(response, res_data)

        except Exception as err:
            if isinstance(err, PyperImporterError):
                raise err

            raise PyperImporterException(str(err)).with_traceback(err.__traceback__)

    @staticmethod
    def prepare_kwargs_request(**kwargs):
        if 'headers' not in kwargs:
            kwargs.update({'headers': {}})

        if 'params' not in kwargs:
            kwargs.update({'params': {}})

        return kwargs
