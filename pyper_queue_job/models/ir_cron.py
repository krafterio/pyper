# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class IrCron(models.Model):
    _inherit = 'ir.cron'

    queue_job_runner = fields.Boolean(
        help='If checked, the cron is considered to be a Queue Jobs Runner.',
    )
