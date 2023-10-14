# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    queue_job_allow_to_ping_api = fields.Boolean(
        'Queue Job Ping API?',
        default=False,
        help='In order to prevent the hosting platforms from stopping the container because no network action is detected, this option allows you to perform public HTTP pings on the instance in order to simulate network activity when a job is running in progress',
        config_parameter='pyper_queue_job.allow_to_ping_api',
    )
