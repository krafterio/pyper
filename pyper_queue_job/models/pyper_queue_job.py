# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models, Command, _

from datetime import datetime, timedelta

from ..exceptions import QueueJobProcessError, QueueJobError

import xmlrpc

import traceback


class PyperQueueJob(models.Model):
    _name = 'pyper.queue.job'
    _description = "Queue Job"
    _log_access = False
    _order = 'date_enqueued DESC, id desc'

    name = fields.Char(
        'Name',
        required=True,
        readonly=True,
    )

    model_name = fields.Char(
        'Model Name',
        required=True,
        readonly=True,
    )

    model_method = fields.Char(
        'Model method',
        readonly=True,
        default='queue_job_process',
    )

    state = fields.Selection(
        [
            ('enqueued', 'Enqueued'),
            ('doing', 'Doing'),
            ('stopped', 'Stopped'),
            ('done', 'Done'),
            ('failed', 'Failed'),
            ('cancelled', 'Cancelled'),
        ],
        'State',
        readonly=True,
        store=True,
        compute='_compute_state',
    )

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User',
        readonly=True,
        required=True,
        default=lambda self: self.env.user
    )

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        index=True,
        readonly=True,
        default=lambda self: self.env.company
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

    result = fields.Text(
        'Result',
        readonly=True,
        copy=False,
    )

    execution_time = fields.Integer(
        string="Execution Time",
        help='Time required to execute this job in seconds.',
        readonly=True,
        copy=False,
        default=0,
    )

    date_created = fields.Datetime(
        string='Created Date',
        readonly=True,
        default=lambda self: datetime.now(),
        copy=False,
    )

    date_write = fields.Datetime(
        string='Last Updated Date',
        readonly=True,
        default=lambda self: datetime.now(),
        copy=False,
        automatic=True,
    )

    date_enqueued = fields.Datetime(
        string='Date Enqueued',
        readonly=True,
        default=lambda self: datetime.now(),
        copy=False,
    )

    date_started = fields.Datetime(
        string='Start Date',
        readonly=True,
        copy=False,
    )

    date_stopped = fields.Datetime(
        string='Stopped Date',
        readonly=True,
        copy=False,
    )

    date_ended = fields.Datetime(
        string='End Date',
        readonly=True,
        store=True,
        compute='_compute_date_ended',
    )

    date_done = fields.Datetime(
        'Date done',
        readonly=True,
        copy=False,
    )

    date_cancelled = fields.Datetime(
        'Date canceled',
        readonly=True,
        copy=False,
    )

    date_failed = fields.Datetime(
        'Date failed',
        readonly=True,
        copy=False,
    )

    log_ids = fields.One2many(
        'pyper.queue.job.log',
        'queue_job_id',
        'Queue job errors',
        readonly=True,
    )

    log_count = fields.Integer(
        'Log count',
        store=True,
        compute='_compute_log_count',
    )

    log_success_count = fields.Integer(
        'Log success count',
        store=True,
        compute='_compute_log_success_count',
    )

    log_info_count = fields.Integer(
        'Log info count',
        store=True,
        compute='_compute_log_info_count',
    )

    log_warning_count = fields.Integer(
        'Log warning count',
        store=True,
        compute='_compute_log_warning_count',
    )

    log_error_count = fields.Integer(
        'Log error count',
        store=True,
        compute='_compute_log_error_count',
    )

    date_ping_api = fields.Datetime(
        'Date ping API',
        readonly=True,
        copy=False,
    )

    _allow_to_ping_api = fields.Boolean(
        'Allow to ping API?',
        default=False,
        store=False,
        readonly=True,
    )

    _ping_api_interval = fields.Integer(
        'Ping API Interval',
        default=60,
        store=False,
        readonly=True,
    )

    _ping_api_base_url = fields.Char(
        'Ping API Base URL',
        store=False,
        readonly=True,
    )

    @api.depends('date_enqueued', 'date_started', 'date_stopped', 'date_done', 'date_cancelled', 'date_failed')
    def _compute_state(self):
        for job in self:
            if not job.date_started and job.date_ended:
                job.date_started = datetime.now()

            if job.date_done:
                job.state = 'done'
                job.execution_time += (job.date_done - job.date_started).total_seconds()
            elif job.date_cancelled:
                job.state = 'cancelled'
                job.execution_time += (job.date_cancelled - job.date_started).total_seconds()
            elif job.date_failed:
                job.state = 'failed'
                job.execution_time += (job.date_failed - job.date_started).total_seconds()
            elif job.date_stopped:
                job.state = 'stopped'
                job.execution_time += (job.date_stopped - job.date_started).total_seconds()
            elif job.date_started:
                job.state = 'doing'
            else:
                job.state = 'enqueued'

    @api.depends('date_stopped', 'date_done', 'date_cancelled', 'date_failed')
    def _compute_date_ended(self):
        for job in self:
            if job.date_stopped:
                job.date_ended = job.date_stopped
            elif job.date_done:
                job.date_ended = job.date_done
            elif job.date_cancelled:
                job.date_ended = job.date_cancelled
            elif job.date_failed:
                job.date_ended = job.date_failed
            else:
                job.date_ended = False

    @api.depends('log_ids')
    def _compute_log_count(self):
        for item in self:
            item.log_count = len(item.log_ids.ids)

    @api.depends('log_ids')
    def _compute_log_success_count(self):
        for item in self:
            search_domain = [('queue_job_id', '=', item.id), ('type', '=', 'success')]
            item.log_success_count = item.log_ids.search_count(search_domain) if len(item.log_ids.ids) > 0 else 0

    @api.depends('log_ids')
    def _compute_log_info_count(self):
        for item in self:
            search_domain = [('queue_job_id', '=', item.id), ('type', '=', 'info')]
            item.log_info_count = item.log_ids.search_count(search_domain) if len(item.log_ids.ids) > 0 else 0

    @api.depends('log_ids')
    def _compute_log_warning_count(self):
        for item in self:
            search_domain = [('queue_job_id', '=', item.id), ('type', '=', 'warning')]
            item.log_warning_count = item.log_ids.search_count(search_domain) if len(item.log_ids.ids) > 0 else 0

    @api.depends('log_ids')
    def _compute_log_error_count(self):
        for item in self:
            search_domain = [('queue_job_id', '=', item.id), ('type', '=', 'error')]
            item.log_error_count = item.log_ids.search_count(search_domain) if len(item.log_ids.ids) > 0 else 0

    def write(self, values):
        values.update({
            'date_write': self.env.cr.now()
        })
        return super().write(values)

    def action_view_queue_job_successes(self):
        return self.action_view_queue_job_logs('success')

    def action_view_queue_job_infos(self):
        return self.action_view_queue_job_logs('info')

    def action_view_queue_job_warnings(self):
        return self.action_view_queue_job_logs('warning')

    def action_view_queue_job_errors(self):
        return self.action_view_queue_job_logs('error')

    def action_view_queue_job_logs(self, log_type=None):
        self.ensure_one()

        domain = [('queue_job_id', '=', self.id)]

        if log_type:
            domain.append(('type', '=', log_type))

        return {
            'name': _('Queue Job Logs'),
            'type': 'ir.actions.act_window',
            'res_model': 'pyper.queue.job.log',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': domain,
        }

    def _run(self):
        for job in self:
            if job.state not in ['enqueued']:
                continue

            job.date_started = datetime.now()

    def _fail(self, exception_name, exception_message=False, exception_info=False):
        for job in self:
            job.date_failed = datetime.now()
            job.exception_name = exception_name
            job.exception_message = exception_message
            job.exception_info = exception_info

    def _done(self, result=False):
        for job in self:
            if job.state not in ['doing']:
                continue

            job.date_done = datetime.now()
            job.result = result

    def log_success(self, message=False, info=False, payload=False, auto_commit=False):
        name = 'LogSuccess' if message else False
        self._log('success', name, message, info, payload, auto_commit)

    def log_info(self, name, message=False, info=False, payload=False, auto_commit=False):
        self._log('info', name, message, info, payload, auto_commit)

    def log_warning(self, name, message=False, info=False, payload=False, auto_commit=False):
        self._log('warning', name, message, info, payload, auto_commit)

    def log_error(self, name, message=False, info=False, payload=False, auto_commit=False):
        self._log('error', name, message, info, payload, auto_commit)

    def _log(self, log_type, name=False, message=False, info=False, payload=False, auto_commit=False):
        self.ensure_one()

        if name:
            self.log_ids = [Command.create(self._create_log_vals(log_type, name, message, info, payload))]

        self.ping_api()

        if auto_commit:
            self.env.cr.commit()

    def _create_log_vals(self, log_type, name=False, message=False, info=False, payload=False):
        return {
            'type': log_type,
            'queue_job_id': self.id,
            'name': name,
            'message': message,
            'info': info,
        }

    def schedule_now(self):
        now = datetime.now()
        for job in self:
            if job.state not in ['enqueued']:
                continue

            job.date_enqueued = now

    def cancel(self):
        for job in self:
            if job.state not in ['enqueued', 'doing', 'stopped']:
                continue

            job.date_cancelled = datetime.now()

    def stop(self):
        for job in self:
            if job.state not in ['doing']:
                continue

            job.date_stopped = datetime.now()

    def stop_and_schedule(self, date_enqueued: datetime = None):
        now = datetime.now()
        for job in self:
            if job.state not in ['doing']:
                continue

            job.date_done = False
            job.date_cancelled = False
            job.date_stopped = False
            job.date_failed = False
            job.date_started = False
            job.date_enqueued = date_enqueued if date_enqueued else now

    def relaunch(self):
        for job in self:
            if job.state not in ['stopped', 'failed']:
                continue

            self._reset_values(True)

    def retry(self):
        now = datetime.now()
        for job in self:
            if job.state not in ['cancelled', 'failed']:
                continue

            job.date_enqueued = now
            job._reset_values()

    def _reset_values(self, relaunch: bool = False):
        self.ensure_one()
        self.date_started = False
        self.date_stopped = False
        self.date_done = False
        self.date_cancelled = False
        self.date_failed = False
        self.date_ping_api = False
        self.exception_name = False
        self.exception_message = False
        self.exception_info = False

        if not relaunch:
            self.execution_time = 0
            self.log_ids = [Command.clear()]

    def process_one(self):
        self.ensure_one()
        job = (self
               .with_company(self.company_id)
               .with_user(self.user_id)
               .with_context(allowed_company_ids=[self.company_id.id]))
        job._process()

    @api.model
    def runner(self):
        job = self._acquire_next_job()
        while job:
            job._process()
            job = self._acquire_next_job()

    @api.model
    def _acquire_next_job(self):
        max_doing = int(self.env['ir.config_parameter'].sudo().get_param('pyper_queue_job.max_doing_without_action', 20))

        self.env.flush_all()

        try:
            self.env.cr.execute(
                f"""
                SELECT id
                FROM pyper_queue_job
                WHERE state = 'doing'
                    AND date_write >= (now() AT TIME ZONE 'UTC' - interval '{max_doing} seconds')
                ORDER BY date_started
                LIMIT 1 FOR NO KEY UPDATE SKIP LOCKED
                """
            )

            row = self.env.cr.fetchone()

            if row and row[0]:
                return False

            self.env.cr.execute(
                f"""
                SELECT id
                FROM pyper_queue_job
                WHERE (state = 'enqueued' AND (date_enqueued IS NULL OR date_enqueued <= (now() AT TIME ZONE 'UTC')))
                    OR (state = 'doing' AND date_write < (now() AT TIME ZONE 'UTC' - interval '{max_doing} seconds'))
                ORDER BY state, date_enqueued
                LIMIT 1 FOR NO KEY UPDATE SKIP LOCKED
                """
            )

            row = self.env.cr.fetchone()
            job = self.browse(row and row[0])
            # Process the job with the defined company and user in job
            job = job\
                .with_company(job.company_id)\
                .with_user(job.user_id)\
                .with_context(allowed_company_ids=[job.company_id.id])

            return job
        except Exception:
            self.env.cr.rollback()
            return False

    def _process(self):
        self.ensure_one()

        self._run()
        self.env.cr.commit()

        self.ping_api()

        try:
            if self.model_name not in self.env:
                raise QueueJobProcessError(_('The model name does not exist'))

            model = self.env[self.model_name]

            if not hasattr(model, self.model_method):
                raise QueueJobProcessError(_('The model method does not exist in model'))

            getattr(model, self.model_method)(self)
            self._done()
        except Exception as err:
            msg = _('Job interrupted by unknown exception')
            fail_tracback = traceback.format_exc() if not isinstance(err, QueueJobError) else False

            if str(err):
                msg = str(err)

            self._fail(type(err).__name__, msg, fail_tracback)

    def ping_api(self):
        if not self._ping_api_base_url:
            # Initialize ping config only the first time
            config = self.env['ir.config_parameter'].sudo()
            self._allow_to_ping_api = bool(config.get_param('pyper_queue_job.allow_to_ping_api', False))
            self._ping_api_interval = int(config.get_param('pyper_queue_job.ping_api.interval', 60))
            self._ping_api_base_url = config.get_param('web.base.url')

        if not self._allow_to_ping_api:
            return

        if self.date_ping_api is not False and (self.date_ping_api + timedelta(seconds=self._ping_api_interval)) > datetime.now():
            return

        self.date_ping_api = datetime.now()

        try:
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self._ping_api_base_url))
            common.version()
        except Exception as err:
            msg = _('Impossible to ping the API')
            fail_tracback = traceback.format_exc() if not isinstance(err, QueueJobError) else False

            self.log_warning(
                'PingApi',
                msg,
                fail_tracback,
                auto_commit=True
            )
