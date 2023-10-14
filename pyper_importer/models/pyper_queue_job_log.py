# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class PyperQueueJobLog(models.Model):
    _inherit = 'pyper.queue.job.log'

    type = fields.Selection(
        selection_add=[
            ('skip', 'Skip'),
        ],
        ondelete={'skip': 'set default'},
    )

    offset = fields.Integer(
        'Offset',
        default=0,
        required=True,
        readonly=True,
    )

    origin_identifier = fields.Char(
        'Origin identifier',
        readonly=True,
    )

    target_identifier = fields.Char(
        'Target identifier',
        readonly=True,
    )
