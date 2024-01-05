# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models

from yaml import dump as yaml_dump


class PyperQueueJob(models.Model):
    _inherit = 'pyper.queue.job'

    log_skip_count = fields.Integer(
        'Log skip count',
        store=True,
        compute='_compute_log_skip_count',
    )

    importer_provider_id = fields.Many2one(
        'pyper.importer.provider',
        'Provider',
        readonly=True,
        ondelete='cascade',
    )

    importer_endpoint_id = fields.Many2one(
        'pyper.importer.endpoint',
        'Endpoint',
        readonly=True,
        ondelete='cascade',
    )

    importer_allow_update = fields.Boolean(
        'Importer allow update?',
        readonly=True,
        default=False,
    )

    importer_batch_size = fields.Integer(
        'Importer batch size',
        readonly=True,
        help='If value is zero, no batch is applied',
    )

    importer_max_offset = fields.Integer(
        'Importer max offset',
        readonly=True,
        default=0,
        help='If value is zero, no limit is applied',
    )

    importer_start_offset = fields.Integer(
        'Importer start offset',
        readonly=True,
        default=0,
    )

    importer_latest_offset = fields.Integer(
        'Importer latest offset',
        readonly=True,
        default=0,
        copy=False,
        help='The latest known offset',
    )

    importer_success_count = fields.Integer(
        'Importer success count',
        readonly=True,
        default=0,
        copy=False,
    )

    importer_skip_count = fields.Integer(
        'Importer skip count',
        readonly=True,
        default=0,
        copy=False,
    )

    importer_error_count = fields.Integer(
        'Importer error count',
        readonly=True,
        default=0,
        copy=False,
    )

    importer_stop_required = fields.Boolean(
        'Check if job must be stopped',
        readonly=True,
        compute='_compute_importer_stop_required',
    )

    @api.depends('state', 'importer_latest_offset', 'importer_start_offset', 'importer_max_offset')
    def _compute_importer_stop_required(self):
        for item in self:
            offset = item.importer_latest_offset
            max_offset = item.importer_max_offset - item.importer_start_offset
            item.importer_stop_required = item.state not in ['doing'] or (0 < max_offset <= offset)

    @api.depends('log_ids')
    def _compute_log_skip_count(self):
        for item in self:
            search_domain = [('queue_job_id', '=', item.id), ('type', '=', 'skip')]
            item.log_skip_count = item.log_ids.search_count(search_domain) if len(item.log_ids.ids) > 0 else 0

    @api.onchange('importer_endpoint_id')
    def _onchange_importer_endpoint_id(self):
        self.importer_batch_size = self.importer_endpoint_id.default_batch_size

        if self.importer_batch_size == 0:
            self.importer_batch_size = int(self.env['ir.config_parameter'].sudo()
                                           .get_param('pyper_importer.default_batch_size', 100))

    def _reset_values(self, relaunch: bool = False):
        super()._reset_values(relaunch)

        if not relaunch:
            self.importer_success_count = 0
            self.importer_skip_count = 0
            self.importer_error_count = 0
            self.importer_latest_offset = 0
        elif self.state in ['failed'] and self.importer_latest_offset > 1 and self.importer_error_count > 1:
            self.importer_latest_offset -= 1

    def log_skip(self, message=False, info=False, payload=False, auto_commit=False, name=False):
        if not name:
            name = 'LogSkip' if message else False
        self.importer_latest_offset += 1
        self.importer_skip_count += 1
        self._log('skip', name, message, info, payload, auto_commit)

    def log_success(self, message=False, info=False, payload=False, auto_commit=False):
        self.importer_latest_offset += 1
        self.importer_success_count += 1
        super().log_success(message, info, payload, auto_commit)

    def log_error(self, error_name, error_message=False, error_info=False, payload=False, auto_commit=False):
        self.importer_latest_offset += 1
        self.importer_error_count += 1
        super().log_error(error_name, error_message, error_info, payload, auto_commit)

    def _create_log_vals(self, log_type, name=False, message=False, info=False, payload=False):
        if payload and 'item' in payload:
            info = (info + "\n\n" if info else '') + yaml_dump({'Item': payload.get('item')})

        if payload and 'payload' in payload:
            info = (info + "\n\n" if info else '') + yaml_dump({'Payload': payload.get('payload')})

        vals = super()._create_log_vals(log_type, name, message, info, payload)
        vals.update({
            'offset': self.importer_latest_offset,
        })

        if type(payload) is dict:
            vals.update({
                'origin_identifier': payload.get('origin_identifier', False),
                'target_identifier': payload.get('target_identifier', False),
            })

        return vals

    def action_view_queue_job_skipped(self):
        return self.action_view_queue_job_logs('skip')
