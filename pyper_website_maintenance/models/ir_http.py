# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models
from odoo.http import request


class Http(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _serve_fallback(cls):
        response = super()._serve_fallback()
        under_maintenance = cls._redirect_under_maintenance()
        return under_maintenance if under_maintenance else response

    @classmethod
    def _dispatch(cls, endpoint):
        under_maintenance = cls._redirect_under_maintenance()
        return under_maintenance if under_maintenance else super()._dispatch(endpoint)

    @classmethod
    def _redirect_under_maintenance(cls):
        website = (request.website if hasattr(request, 'website') else request.env['website']).sudo()

        if (request.is_frontend
                and not request.env.user.has_group('base.group_user')
                and website.is_under_maintenance
                and website.under_maintenance_page
                and request.httprequest.path not in cls._get_under_maintenance_allowed_paths(website)):
            return request.redirect(website.under_maintenance_page.url, code=302)

        return None

    @classmethod
    def _get_under_maintenance_allowed_paths(cls, website):
        return [
            '/web/login',
            website.under_maintenance_page.url,
        ]
