# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models, _

from datetime import datetime


class PyperImportScheduleWizard(models.TransientModel):
    _name = 'pyper.importer.schedule_wizard'
    _description = 'Wizard to schedule a job of Importer Provider'

    importer_provider_ids = fields.Many2many(
        'pyper.importer.provider',
        string='Importer Provider',
    )

    importer_provider_count = fields.Integer(
        'Importer Provider Count',
        compute='_compute_importer_provider_count',
    )

    scheduled_date = fields.Datetime(
        'Scheduled date',
        help='Keep empty this field to run import as soon as possible',
    )

    batch_size = fields.Integer(
        'Batch size',
        required=True,
        default=lambda self: int(self.env['ir.config_parameter'].sudo().get_param('pyper_importer.default_batch_size', 100)),
    )

    max_offset = fields.Integer(
        'Max offset',
        required=True,
        default=0,
        help='If value is zero, no limit is applied',
    )

    start_offset = fields.Integer(
        'Start offset',
        required=True,
        default=0,
    )

    user_id = fields.Many2one(
        'res.users',
        'Context user',
        required=True,
        default=lambda self: self.env.user,
    )

    company_ids = fields.Many2many(
        'res.company',
        string='Context companies',
        required=True,
        help='Companies used for selected import providers'
    )

    allow_update = fields.Boolean(
        'Allow update?',
        default=False,
        help='Allow update existing record if provider is compatible with this feature',
    )

    display_allow_update = fields.Boolean(
        'Display Allow update field?',
        compute='_compute_display_allow_update',
    )

    @api.depends('importer_provider_ids')
    def _compute_importer_provider_count(self):
        for item in self:
            item.importer_provider_count = len(item.importer_provider_ids.ids)

    @api.depends('importer_provider_ids.allow_update')
    def _compute_display_allow_update(self):
        for item in self:
            item.display_allow_update = False

            for import_line in item.importer_provider_ids:
                if import_line.allow_update:
                    item.display_allow_update = True
                    break

    @api.onchange('importer_provider_ids')
    def _onchange_importer_provider_ids(self):
        if self.importer_provider_count > 0:
            self.company_ids = self.importer_provider_ids.default_company_ids

        if len(self.company_ids.ids) == 0:
            self.company_ids = [self.env.company.id]

    def action_schedule_import_job(self):
        self.ensure_one()

        scheduled_date = self.scheduled_date if self.scheduled_date is not False \
            and self.scheduled_date > datetime.now() else datetime.now()

        batch_size = self.batch_size

        if batch_size <= 0:
            batch_size = int(self.env['ir.config_parameter'].sudo().get_param('pyper_importer.default_batch_size', 100))

        companies = []
        for company in self.company_ids:
            companies.append(company)

        for importer_provider in self.importer_provider_ids:
            for company in companies:
                self.env['pyper.queue.job'].create({
                    'name': _('Import: %s for %s', importer_provider.name, company.name),
                    'model_name': importer_provider._name,
                    'user_id': self.user_id.id,
                    'company_id': company.id,
                    'date_enqueued': scheduled_date,
                    'importer_allow_update': importer_provider.allow_update and self.allow_update,
                    'importer_provider_id': importer_provider.id,
                    'importer_batch_size': batch_size,
                    'importer_max_offset': self.max_offset,
                    'importer_start_offset': self.start_offset,
                })

        return {
            'type': 'ir.actions.act_window_close',
        }
