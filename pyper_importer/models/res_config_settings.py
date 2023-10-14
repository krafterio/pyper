# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    active_pyper_importer_endpoint_count = fields.Integer(
        'Number of Active Importer Endpoints',
        compute='_compute_active_pyper_importer_endpoint_count',
    )

    active_pyper_importer_provider_count = fields.Integer(
        'Number of Active Importer Providers',
        compute='_compute_active_pyper_importer_provider_count',
    )

    @api.depends('company_id')
    def _compute_active_pyper_importer_endpoint_count(self):
        active_endpoint_count = self.env['pyper.importer.endpoint'].sudo().search_count([('active', '=', True)])
        for record in self:
            record.active_pyper_importer_endpoint_count = active_endpoint_count

    @api.depends('company_id')
    def _compute_active_pyper_importer_provider_count(self):
        active_provider_count = self.env['pyper.importer.provider'].sudo().search_count([('active', '=', True)])
        for record in self:
            record.active_pyper_importer_provider_count = active_provider_count
