# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import fields, models, _

from datetime import datetime


class PyperQueueJobLog(models.Model):
    _name = 'pyper.queue.job.log'
    _description = 'Queue Job Log'
    _order = 'create_date DESC, id asc'

    queue_job_id = fields.Many2one(
        'pyper.queue.job',
        'Queue Job',
        required=True,
        readonly=True,
        ondelete='cascade',
    )

    type = fields.Selection(
        [
            ('success', 'Success'),
            ('info', 'Info'),
            ('warning', 'Warning'),
            ('error', 'Error'),
        ],
        'Type',
        default='info',
        required=True,
        readonly=True,
    )

    date = fields.Datetime(
        string='Date',
        readonly=True,
        default=lambda self: datetime.now(),
        copy=False,
    )

    name = fields.Char(
        string='Name',
        readonly=True,
        copy=False,
    )

    message = fields.Char(
        string='Message',
        readonly=True,
        copy=False,
    )

    info = fields.Text(
        string='Info',
        readonly=True,
        copy=False,
    )

    def name_get(self):
        res = []
        for log in self:
            name = _('Log #') + str(log.id) + ' - ' + log.queue_job_id.name
            res.append((log.id, name))

        return res
