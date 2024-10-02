# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_spam_protected = fields.Boolean(
        "Is spam protected",
        tracking=True
    )

    def check_spam_protection(self):
        self.env['piloterr.domain.dnsbl.checker'].check_spam(
            delay=False,
            callback='set_company_technology',
            model_name=self._name,
            obj_id=self.id,
            field_name='is_spam_protected'
        )

    def check_multiple_contacts_spam_protection(self):
        if len(self.ids) == 1:
            delay = False
        else:
            delay = True
        self.env['piloterr.domain.dnsbl.checker'].check_multiple_spam(
            delay=delay,
            callback='set_company_technology',
            model_name=self._name,
            obj_id=self.mapped('id'),
            field_name='is_spam_protected'
        )
