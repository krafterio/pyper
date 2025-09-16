# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Format phone and mobile fields separately because phone_sanitized use phone field or mobile field
    phone_formatted = fields.Char(
        'Phone formatted',
        compute='_compute_phone_formatted',
        compute_sudo=True,
        store=True,
    )

    mobile_formatted = fields.Char(
        'Mobile formatted',
        compute='_compute_mobile_formatted',
        compute_sudo=True,
        store=True,
    )

    @api.depends('phone')
    def _compute_phone_formatted(self):
        for record in self:
            record.phone_formatted = record._phone_format(fname='phone') if record.phone else False

    @api.depends('mobile')
    def _compute_mobile_formatted(self):
        for record in self:
            record.mobile_formatted = record._phone_format(fname='mobile') if record.mobile else False
