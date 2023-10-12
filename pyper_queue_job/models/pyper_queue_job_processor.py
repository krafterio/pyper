# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import models


class PyperQueueJobProcessor(models.AbstractModel):
    _name = 'pyper.queue.job.processor'
    _description = 'Queue Job Processor'

    @staticmethod
    def queue_job_process(job):
        pass
