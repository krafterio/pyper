# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models, fields, api


class TicketConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ticket_validator = fields.Boolean(string='Ticket Validator')

    def get_values(self):
        res = super(TicketConfigSettings, self).get_values()
        res['ticket_validator'] = self.env['ir.config_parameter'].sudo().get_param('ticketing.ticket_validator', default=False)
        return res

    def set_values(self):
        super(TicketConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('ticketing.ticket_validator', self.ticket_validator)