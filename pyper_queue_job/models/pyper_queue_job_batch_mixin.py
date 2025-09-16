# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

import traceback

from odoo import fields, models, _


class PyperQueueJobBatchMixin(models.AbstractModel):
    _name = 'pyper.queue.job.batch.mixin'
    _description = 'Queue Job Batch Mixin'
    _order = 'create_date DESC'

    state = fields.Selection(
        [
            ('enqueued', 'Enqueued'),
            ('in_progress', 'In progress'),
            ('waiting', 'Waiting'),
            ('done', 'Done'),
            ('failed', 'Failed'),
        ],
        'State',
        default='enqueued',
        readonly=True,
        store=True,
    )

    exception_name = fields.Char(
        string='Exception',
        readonly=True,
        copy=False,
    )

    exception_message = fields.Char(
        string='Exception Message',
        readonly=True,
        copy=False,
    )

    exception_info = fields.Text(
        string='Exception Info',
        readonly=True,
        copy=False,
    )

    def retry(self):
        for batch in self:
            if batch._reset_values():
                self.with_delay().retrieve_info()

    def _reset_values(self):
        self.ensure_one()
        self.exception_name = False
        self.exception_message = False
        self.exception_info = False

        return True

    def _raise_exception(self, exception):
        self.state = 'failed'

        msg = _('Batch interrupted by unknown exception')
        fail_tracback = traceback.format_exc() if not isinstance(exception, PyperQueueJobBatchMixin) else False

        if str(exception):
            msg = str(exception)

        self.exception_name = type(exception).__name__
        self.exception_message = msg
        self.exception_info = fail_tracback

        self.env.cr.commit()
        raise exception
