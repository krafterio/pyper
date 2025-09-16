# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import api, models


class BaseModel(models.AbstractModel):
    _inherit = 'base'

    # ------------------------------------------------------------
    # FIELDS HELPERS
    # ------------------------------------------------------------

    def _phone_format(self, fname=False, number=False, country=False, force_format='E164', raise_exception=False):
        sms_country_field_name = self.env.context.get('sms_country_field_name', False)

        if not country and sms_country_field_name:
            country = self[sms_country_field_name]

        return super()._phone_format(fname, number, country, force_format, raise_exception)

    @api.model
    def _mail_get_partner_fields(self, introspect_fields=False):
        if self.env.context.get('sms_disable_partner_link', False):
            return []

        return super()._mail_get_partner_fields(introspect_fields)
