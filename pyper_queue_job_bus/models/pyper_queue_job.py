# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import _, models


class PyperQueueJob(models.Model):
    _inherit = 'pyper.queue.job'

    def notify(self, message: str, title: str = None, notif_type: str = 'info'):
        self.ensure_one()
        self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
            'type': notif_type,
            'title': title if title else _('Delayed action'),
            'message': message,
        })

        return self
