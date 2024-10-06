# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from bs4 import BeautifulSoup


class resPartnerRequest(models.Model):
    _name = 'res.partner.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    description = fields.Html(string='Description')
    author_id = fields.Many2one('res.partner', string='Created By', default=lambda self: self.env.user.partner_id, readonly=True)
    author_parent_id = fields.Many2one('res.partner', string='Company', related='author_id.parent_id')
    state = fields.Selection([
        ('waiting_for_validation', 'Waiting for validation'),
        ('awaiting_requalification', 'Awaiting requalification'),
        ('to_be_processed', 'To be processed'),
        ('in_progress', 'In progress'),
        ('pending', 'Pending'),
        ('closed', 'Closed'),
    ], string='State', default='waiting_for_validation', group_expand='_expand_groups', track_visibility='onchange')
    create_date = fields.Datetime(string='Created Date', readonly=True)
    priority = fields.Selection(
        [
            ('low', 'Low'),
            ('normal', 'Normal'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ], string='Priority', default='low', required=True)
    category = fields.Selection(
        [
            ('incident', 'Incident'),
            ('service request', 'Service Request'),
            ('information request', 'Information Request'),
            ('training request', 'Training Request'),
        ], string='Category', required=True)
    is_validated = fields.Boolean(string='Is Validated', default=False)
    description_text = fields.Text(string='Description Text', compute='_compute_description_text')
    is_frontend_multilang = fields.Boolean(default=False)

    @api.model_create_multi
    def create(self, vals_list):
        requests = super().create(vals_list)
        for request in requests:
            is_request_validator_enabled = request.author_parent_id.require_request_approval
            if is_request_validator_enabled and request.author_parent_id:
                request.send_notification_to_validator()
            else:
                request.is_validated = True
                request.state = 'to_be_processed'
        return requests

    def write(self, vals):
        res = super().write(vals)
        if 'state' in vals:
            closed_requests = self.filtered(lambda r: r.state == 'closed')
            for request in closed_requests:
                request.send_notification(
                    subject=_('Request closed'),
                    body=_('The request has been closed.')
                )
        return res

    def send_notification(self, subject, body):
        partner_followers = self.message_follower_ids.mapped('partner_id')
        self.sudo().message_notify(
            subject=subject,
            body=body,
            partner_ids=partner_followers.ids
        )
    
    def send_notification_to_validator(self):
        group_id = self.env.ref('pyper_partner_request.group_request_validator')
        users = self.env['res.users'].search([('groups_id', 'in', group_id.id)])
        partner_ids = [user.partner_id.id for user in users]


        self.sudo().message_subscribe(partner_ids=partner_ids)
        self.sudo().send_notification(
            subject=_('New request to validate'),
            body=_('A new request has been created and requires validation.')
        )

    def action_validate(self):
        if not self.env.user.has_group('pyper_partner_request.group_request_validator'):
            raise UserError(_('You do not have the necessary permissions to validate this request.'))
        self.is_validated = True
        self.state = 'to_be_processed'
        self.message_post(body=_('Request validated by %s' % self.env.user.name))

    def action_close(self):
        self.state = 'closed'
        self.message_post(body=_('Request closed by %s' % self.env.user.name))

    def action_ask_requalification(self):
        self.state = 'awaiting_requalification'
        self.message_post(body=_('Request requalification asked by %s' % self.env.user.name))

    @api.depends('description')
    def _compute_description_text(self):
        for record in self:

            if record.description:
                soup = BeautifulSoup(record.description, 'html.parser')
                record.description_text = soup.get_text()
            else:
                record.description_text = ''
    @api.model
    def _expand_groups(self, states, domain, order):
        return   ['to_be_processed', 'in_progress', 'pending', 'done']
