# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models, fields, api


class Ticket(models.Model):
    _name = 'ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user, readonly=True)
    company_id = fields.Many2one('res.company', string='Company', related='user_id.company_id', readonly=True)
    status = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In progress'),
        ('done', 'Done'),
    ], string='Status', default='new')
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High'),
    ], string='Priority', default='1', required=True)