# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import http

from odoo.addons.pyper_queue_job.exceptions import QueueJobException, QueueJobError


class PyperImporterException(QueueJobException):
    """Generic error managed by the Pyper importer with traceback.
    """
    pass


class PyperImporterError(QueueJobError):
    """Generic error managed by the Pyper importer without traceback.
    """
    pass


class PyperImporterConfigurationError(PyperImporterError):
    pass


class PyperImporterJSONDecodeError(PyperImporterError):
    pass


class PyperImporterHttpError(PyperImporterError):
    def __init__(self, status_code: int, message: str = None):
        """
        :param message: exception message and frontend modal content
        """
        if not message:
            message = http.client.responses[status_code]

        super().__init__(message)
        self.status_code = status_code


class PyperImporterAuthenticationError(PyperImporterHttpError):
    def __init__(self, message: str = None):
        super().__init__(http.HTTPStatus.UNAUTHORIZED, message)


class PyperImporterAuthorizationError(PyperImporterHttpError):
    def __init__(self, message: str = None):
        super().__init__(http.HTTPStatus.FORBIDDEN, message)
