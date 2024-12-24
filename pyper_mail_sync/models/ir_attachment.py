# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    restrict_access = fields.Boolean(
        string='Restrict Access',
        compute='_compute_restrict_access',
        store=True,
    )

    access_partner_ids = fields.Many2many(
        'res.partner',
        string='Access Partners',
    )

    @api.depends('access_partner_ids')
    def _compute_restrict_access(self):
        for record in self:
            record.restrict_access = len(record.access_partner_ids) > 0
