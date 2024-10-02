# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models


class Respartner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner', 'piloterr.mixin']

    def search_email(self):
        self.env['piloterr.email.finder'].retrieve_mail(
            delay=False,
            callback='set_email',
            model_name=self._name,
            obj_id=self.id,
            field_name='email'
        )

    def search_many_emails(self):
        if len(self.ids) == 1:
            delay = False
        else:
            delay = True
        self.env['piloterr.email.finder'].retrieve_many_mail(
            delay=delay,
            callback='set_email',
            model_name=self._name,
            obj_id=self.mapped('id'),
            field_name='email'
        )
