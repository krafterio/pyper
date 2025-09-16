# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

import inspect

from odoo.addons.web.controllers.dataset import DataSet
from odoo.http import request
from ..models.models import SecuredBase, CONTEXT_CHECK_FIELD_ACCESS_RIGHTS


def get_public_methods(cls):
    methods = inspect.getmembers(cls, predicate=inspect.isfunction)

    return [
        name for name, func in methods
        if not name.startswith('_') and func.__qualname__.startswith(cls.__name__ + '.')
    ]


SECURED_METHODS = get_public_methods(SecuredBase)


class AccessDataSet(DataSet):
    def _call_kw(self, model, method, args, kwargs):
        """
        Secure only the call of overridden methods to include access rights management.
        """
        if method in SECURED_METHODS:
            context = kwargs.get('context', {})
            context.update({CONTEXT_CHECK_FIELD_ACCESS_RIGHTS: not request.env.su})
            kwargs.update({'context': context})

        return super()._call_kw(model, method, args, kwargs)
