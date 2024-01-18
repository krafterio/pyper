# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from datetime import datetime

from dateutil import parser

from io import StringIO

from html.parser import HTMLParser

from odoo import api, fields, models, _

from odoo.addons.pyper_queue_job.exceptions import QueueJobError

from ..exceptions import PyperImporterError
from ..providers import AllowUpdateConfigurableProvider, BatchableProvider, SkippedRecordsLoggableProvider
from ..tools import property_path

import importlib

import traceback


class HtmlStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()


class PyperImporterProvider(models.Model):
    _name = 'pyper.importer.provider'
    _description = 'Run import from a Provider'
    _inherit = ['pyper.queue.job.processor']
    _order = 'sequence asc, id asc'

    active = fields.Boolean(
        'Active',
        default=True,
    )

    sequence = fields.Integer(
        'Sequence',
        default=10,
    )

    name = fields.Char(
        'Name',
        required=True,
        readonly=True,
    )

    module_name = fields.Char(
        'Module name',
        required=True,
        readonly=True,
    )

    class_name = fields.Char(
        'Class name',
        required=True,
        readonly=True,
    )

    default_endpoint_id = fields.Many2one(
        'pyper.importer.endpoint',
        'Default endpoint',
        help='Allows you to pre-fill the endpoint field in the wizard to launch an import',
    )

    default_company_ids = fields.Many2many(
        'res.company',
        'res_company_pyper_importer_providers_rel',
        'importer_provider_id',
        'cid',
        string='Default companies',
        help='If this field is empty, all companies available for the import are used',
    )

    queue_job_ids = fields.One2many(
        'pyper.queue.job',
        'importer_provider_id',
        'Queue jobs',
        readonly=True,
    )

    opened_queue_job_count = fields.Integer(
        'Opened queue job count',
        compute='_compute_opened_queue_job_count',
    )

    allow_update = fields.Boolean(
        'Allow update?',
        readonly=True,
        store=True,
        compute='_compute_allow_update',
    )

    log_skipped_records = fields.Boolean(
        'Log skipped records?',
        store=True,
        compute='_compute_log_skipped_records'
    )

    @api.depends('queue_job_ids')
    def _compute_opened_queue_job_count(self):
        for item in self:
            item.opened_queue_job_count = self.env['pyper.queue.job'].search_count([
                ('importer_provider_id', '=', item.id),
                ('state', 'in', ['enqueued', 'doing', 'stopped']),
            ])

    @api.depends('module_name', 'class_name')
    def _compute_log_skipped_records(self):
        for item in self:
            try:
                module = importlib.import_module('odoo.addons.' + item.module_name)
                cls = getattr(module, item.class_name)
                provider = cls(self.env, self.env['pyper.queue.job'])
                item.log_skipped_records = isinstance(provider, SkippedRecordsLoggableProvider)
            except Exception:
                item.log_skipped_records = False

    @api.depends('module_name', 'class_name')
    def _compute_allow_update(self):
        for item in self:
            try:
                module = importlib.import_module('odoo.addons.' + item.module_name)
                cls = getattr(module, item.class_name)
                provider = cls(self.env, self.env['pyper.queue.job'])
                item.allow_update = isinstance(provider, AllowUpdateConfigurableProvider)
            except Exception:
                item.allow_update = False

    def action_view_queue_jobs(self):
        self.ensure_one()

        return {
            'name': _('Queue Jobs'),
            'type': 'ir.actions.act_window',
            'res_model': 'pyper.queue.job',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [
                ('importer_provider_id', '=', self.id),
            ]
        }

    def action_schedule_run(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Schedule a run'),
            'res_model': 'pyper.importer.schedule_wizard',
            'view_mode': 'form',
            'target': 'new',
            'view_id': self.env.ref('pyper_importer.pyper_importer_schedule_wizard_form', False).id,
            'context': {**self.env.context, **{
                'dialog_size': 'large',
                'default_importer_provider_ids': self.ids,
            }},
        }

    def button_schedule_run(self):
        self.ensure_one()
        return self.action_schedule_run()

    def _except_load_exception(self, job, err: Exception, item: dict, origin_identifier: str, existing_item=False,
                               payload: dict = False):
        """
        :param job (Model<pyper.queue.job>): the queue job
        """
        self.env.cr.rollback()
        err_type = type(err).__name__

        # SerializationFailure exception is thrown when job is stopped and should not be logged
        if err_type == 'SerializationFailure':
            return

        msg = _('Import interrupted by unknown exception')
        fail_tracback = traceback.format_exc() if not isinstance(err, QueueJobError) else False

        if str(err):
            msg = str(err)

        job.log_error(
            err_type,
            msg,
            fail_tracback,
            auto_commit=True,
            payload=self._create_log_payload(item, origin_identifier, existing_item, payload)
        )

    @staticmethod
    def _create_log_payload(item: dict, origin_identifier: str, existing_item=False, payload: dict = False) -> dict:
        """
        :param item:             dict        The origin item
        :param origin_identifier str         The origin identifier name
        :param existing_item:    model.Model The existing record
        :return: dict
        """
        res = {
            'item': item,
            'origin_identifier': property_path(item, origin_identifier, False),
            'target_identifier': existing_item.id if existing_item is not False else False,
        }

        if payload:
            if 'origin_identifier' in payload:
                res.update({'origin_identifier': payload.get('origin_identifier')})

            if 'target_identifier' in payload:
                res.update({'target_identifier': payload.get('target_identifier')})

            log_payload = payload.copy()
            if 'origin_identifier' in log_payload:
                log_payload.pop('origin_identifier')
            if 'target_identifier' in log_payload:
                log_payload.pop('target_identifier')
            if 'offset' in log_payload:
                log_payload.pop('offset')
            if 'started_date' in log_payload:
                log_payload.pop('started_date')
            if len(log_payload) > 0:
                res['payload'] = log_payload

        return res

    def search_record(self, model: str, domain: list = None, context: dict = None, sudo: bool = False,
                      order: str = None):
        """
        :return: models.Model
        """
        if domain is None:
            domain = []

        env_model = self.env[model]

        if context is not None:
            env_model = env_model.with_context(**context)

        if 'active' in env_model._fields:
            domain.append(('active', 'in', [True, False]))

        if sudo:
            env_model = env_model.sudo()

        return env_model.search(domain, limit=1, order=order)

    def search_record_id(self, model: str, domain: list = None, context: dict = None, sudo: bool = False,
                         order: str = None):
        return self.search_record(model, domain, context, sudo, order)

    def find_record(self, model: str, identifier_field: str, identifier_value, domain: list = None,
                    context: dict = None, sudo: bool = False, order: str = None):
        """
        :return: models.Model
        """
        if domain is None:
            domain = []

        if identifier_value.__class__ is str:
            identifier_value = identifier_value.strip()

        domain.append((identifier_field, '=', identifier_value))

        if not identifier_value:
            return self.env[model]

        return self.search_record(model, domain, context, sudo, order)

    def find_record_id(self, model: str, identifier_field: str, identifier_value, domain: list = None,
                       context: dict = None, sudo: bool = False, order: str = None):
        return self.find_record(model, identifier_field, identifier_value, domain, context, sudo, order).id

    @staticmethod
    def upsert(item, vals: dict, context: dict = None):
        """
        :param item: (Model<*>) the existing record
        :param vals: dict the new values
        :param context: dict the context for upsert
        :return Model<*>: the created or updated record
        """
        is_create = item.id is False

        if context is None:
            context = {}

        if is_create:
            item = item.with_context(**context).create(vals)
        else:
            item.with_context(**context).write(vals)

        return item

    def override_log_access(self,
                            record: models.Model,
                            create_uid: models.Model | int = None,
                            create_date: datetime = None,
                            write_uid: models.Model | int = None,
                            write_date: datetime = None
                            ):
        record_id = record.id
        record_table = record._table
        sets = []
        params = {}

        if isinstance(create_uid, models.Model):
            create_uid = create_uid.id

        if isinstance(write_uid, models.Model):
            write_uid = write_uid.id

        if create_uid:
            sets.append("create_uid=%(create_uid)s")
            params['create_uid'] = create_uid

        if create_date:
            sets.append("create_date=%(create_date)s")
            params['create_date'] = fields.Datetime.to_string(create_date)

        if write_uid:
            sets.append("write_uid=%(write_uid)s")
            params['write_uid'] = write_uid

        if write_date:
            sets.append("write_date=%(write_date)s")
            params['write_date'] = fields.Datetime.to_string(write_date)

        if sets:
            params['id'] = record_id
            self.env.cr.execute(
                "UPDATE " + record_table + " SET " + ", ".join(sets) + " WHERE id = %(id)s",
                params
            )

    def find_record_by_ext_id(self, external_id: str | bool) -> models.Model | bool:
        if isinstance(external_id, bool):
            return False

        return self.env.ref(external_id, False)

    def find_record_by_gen_ext_id(self, model: str, identifier: str | bool, module: str = None) -> models.Model | bool:
        ext_id = PyperImporterProvider.generate_external_id(model, identifier, module)

        return self.find_record_by_ext_id(ext_id)

    def find_record_id_by_ext_id(self, external_id: str | bool) -> models.Model | bool:
        res = self.find_record_by_ext_id(external_id)

        return res.id if res else False

    def find_record_id_by_gen_ext_id(self, model: str, identifier: str | bool, module: str = None) -> models.Model | bool:
        res = self.find_record_by_gen_ext_id(model, identifier, module)

        return res.id if res else False

    @staticmethod
    def generate_external_id_module(module: str = None) -> str:
        if module is None:
            module = '__importer_data__'

        return str(module).strip().replace(' ', '_').lower()

    @staticmethod
    def generate_external_id_name(model: str, identifier: str | bool) -> str | bool:
        if isinstance(identifier, bool):
            return False

        model = str(model).strip().replace('.', '_')
        identifier = str(identifier).strip()

        for char in ['.', ' ']:
            identifier = identifier.replace(char, '_')

        return model.lower() + '__' + identifier.lower()

    @staticmethod
    def generate_external_id(model: str, identifier: str | bool, module: str = None) -> str | bool:
        name = PyperImporterProvider.generate_external_id_name(model, identifier)

        if isinstance(name, bool):
            return name

        return PyperImporterProvider.generate_external_id_module(module) + '.' + name

    @staticmethod
    def format_datetime(value: str | bool) -> datetime | bool:
        if isinstance(value, bool):
            return value

        return parser.parse(value)

    @staticmethod
    def format_date(value, date_format: str = None, default_value=False):
        val = PyperImporterProvider.format_value(value, default_value)

        if date_format is None:
            date_format = '%Y-%m-%d'

        if val == default_value:
            return val

        try:
            return datetime.strptime(val, date_format)
        except ValueError:
            return default_value

    @staticmethod
    def format_int(value, default_value=False):
        val = PyperImporterProvider.format_value(value, default_value)

        if val == default_value:
            return val

        try:
            return int(val)
        except ValueError:
            return default_value

    @staticmethod
    def format_float(value, default_value=False):
        val = PyperImporterProvider.format_value(value, default_value)

        if val == default_value:
            return val

        try:
            return float(val)
        except ValueError:
            return default_value

    @staticmethod
    def format_value(value, default_value=False):
        if value.__class__ is int or value.__class__ is float or value.__class__ is bool:
            return value

        if value.__class__ is str:
            value = value.strip()

            if value:
                return value

        return default_value

    def strip_html_tag(self, html: str | bool, default_value=False) -> str | bool:
        if html:
            stripper = HtmlStripper()
            stripper.feed(html)
            html = stripper.get_data()

        return self.format_value(html, default_value)

    @staticmethod
    def hash_value(*kwargs) -> str:
        hash_val = ''

        for kwarg in kwargs:
            if kwarg is False:
                hash_val += ''
            else:
                hash_val += str(kwarg).strip()

        return hash_val

    @staticmethod
    def queue_job_process(job):
        importer_provider = job.importer_provider_id

        if importer_provider.id is False:
            raise PyperImporterError(_('Importer provider is not associated with the job'))

        module = importlib.import_module('odoo.addons.' + importer_provider.module_name)
        cls = getattr(module, importer_provider.class_name)

        provider = cls(job.env, job)
        config = job.env['ir.config_parameter'].sudo()

        offset_start = job.importer_start_offset if job.importer_latest_offset == 0 else job.importer_latest_offset
        offset_max = job.importer_max_offset
        offset = offset_start
        batchable = False
        finish = False

        # Init latest offset in job
        if job.importer_latest_offset == 0:
            job.importer_latest_offset = offset

        if isinstance(provider, BatchableProvider):
            batchable = True
            provider.batch_size = job.importer_batch_size

            if provider.batch_size <= 0:
                provider.batch_size = int(config.get_param('pyper_importer.default_batch_size', 100))

            if provider.batch_size > offset_max > 0 and offset >= offset_start:
                provider.batch_size = offset_max

        while finish is False:
            result = []

            if job.importer_stop_required:
                job.importer_latest_offset = offset
                job.env.cr.commit()
                break

            try:
                result = provider.extract(offset, job.date_started)
                finish = len(result) == 0

                if not finish or not batchable:
                    transformed_items = provider.transform(result)
                    provider.load(transformed_items)

                    finish = not batchable
                    # Update offset if ETL actions are successfully
                    offset = job.importer_start_offset
                    offset += job.importer_success_count + job.importer_skip_count + job.importer_error_count
                    job.importer_latest_offset = max(offset, job.importer_latest_offset)
                    job.env.cr.commit()

            except Exception as err:
                # Update offset if ETL actions raise exception
                offset = offset + len(result)
                job.importer_latest_offset = max(offset, job.importer_latest_offset)
                job.env.cr.commit()
                raise err

            # Limit the last batch with the difference between current offset and the max offset
            if offset_max > 0 and isinstance(provider, BatchableProvider):
                next_batch_size = provider.batch_size
                current_offset_max = offset + next_batch_size

                if current_offset_max > offset_max:
                    provider.batch_size = current_offset_max - offset_max

                    if offset >= offset_max:
                        finish = True
