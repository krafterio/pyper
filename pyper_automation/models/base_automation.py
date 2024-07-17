# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import api, fields, models


class BaseAutomation(models.Model):
    _inherit = 'base.automation'

    last_run_edit = fields.Datetime(
        related='last_run',
        compute='_compute_last_run_edit',
        inverse='_inverse_last_run_edit',
        groups='base.group_erp_manager',
    )

    @api.depends('last_run')
    def _compute_last_run_edit(self):
        for automation in self:
            automation.last_run_edit = automation.last_run

    def _inverse_last_run_edit(self):
        for automation in self:
            automation.last_run = automation.last_run_edit
