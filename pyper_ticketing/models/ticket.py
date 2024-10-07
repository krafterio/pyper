# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models, fields, api


class Ticket(models.Model):
    _name = 'ticket'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    user_id = fields.Many2one('res.users', string='User')
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
    ], string='Priority', default='1')