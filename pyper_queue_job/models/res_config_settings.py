# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    queue_job_runner_check_interval = fields.Integer(
        'Queue Job Runner Check Interval',
        default=False,
        help='Allow to not wait for each runner to pass and to check between each interval for the presence of new jobs to be processed (accepted value between 1 and 59 seconds)',
        config_parameter='pyper_queue_job.runner_check_interval',
    )

    queue_job_allow_to_ping_api = fields.Boolean(
        'Queue Job Ping API?',
        default=False,
        help='In order to prevent the hosting platforms from stopping the container because no network action is detected, this option allows you to perform public HTTP pings on the instance in order to simulate network activity when a job is running in progress',
        config_parameter='pyper_queue_job.allow_to_ping_api',
    )
