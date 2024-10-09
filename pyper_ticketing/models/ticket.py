# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models, fields, api, _


class Ticket(models.Model):
    _name = 'ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    partner_id = fields.Many2one('res.partner', string='User', default=lambda self: self.env.user.partner_id, readonly=True)
    parent_id = fields.Many2one('res.partner', string='Company', related='partner_id.parent_id')
    status = fields.Selection([
        ('waiting_for_validation', 'Waiting for validation'),
        ('new', 'New'),
        ('in_progress', 'In progress'),
        ('done', 'Done'),
    ], string='Status', default='new')
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Middle'),
        ('2', 'High'),
    ], string='Priority', default='1', required=True)
    validated = fields.Boolean(string='Validated', default=False)

    @api.model_create_multi
    def create(self, vals_list):
        tickets = super(Ticket, self).create(vals_list)
        for ticket in tickets:
            is_ticket_validator_enabled = self.env['ir.config_parameter'].sudo().get_param('ticketing.ticket_validator', default=False)
            ticket.parent_id = self.env.user.partner_id.parent_id
            ticket.status = 'waiting_for_validation'
            if is_ticket_validator_enabled and ticket.parent_id:
                ticket.send_notification_to_validator()
            else:
                ticket.validated = True
                ticket.status = 'new'
        return tickets

    def send_notification_to_validator(self):
        group_id = self.env.ref('pyper_ticketing.group_ticket_validator')
        users = self.env['res.users'].search([('groups_id', 'in', group_id.id)])
        partner_ids = [user.partner_id.id for user in users]


        self.message_subscribe(partner_ids=partner_ids)
        self.message_post(
            subject=_('New Ticket Created'),
            body=_('A new ticket has been created and requires validation.'),
            message_type='notification',
            subtype_id=self.env.ref('mail.mt_comment').id,
        )

    def action_validate(self):
        self.validated = True
        self.status = 'new'
        self.message_post(body=_('Ticket validated by %s' % self.env.user.name))