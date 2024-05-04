# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    timeline_visible_time_range_start = fields.Float(
        'Visible time range start',
        config_parameter='pyper_timeline.timeline.visibleTimeRangeStart',
    )

    timeline_visible_time_range_end = fields.Float(
        'Visible time range end',
        config_parameter='pyper_timeline.timeline.visibleTimeRangeEnd',
    )
