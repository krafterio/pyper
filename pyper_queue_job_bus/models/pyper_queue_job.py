# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import _, models

from odoo.addons.pyper_queue_job.models.pyper_queue_job import DELAY_AUTO_UNLINK_DONE, DELAY_AUTO_UNLINK_FULL


class PyperQueueJob(models.Model):
    _inherit = 'pyper.queue.job'

    def create(self, vals_list):
        res = super().create(vals_list)
        self._notify_update(res)

        return res

    def write(self, values):
        res = super().write(values)
        self._notify_update_state(self, values)

        return res

    def unlink(self):
        self._notify_update(self)

        return super().unlink()

    def notify(self, message: str = None, title: str = None, notif_type: str = 'info'):
        self.ensure_one()
        self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
            'type': notif_type,
            'title': title if title else _('Delayed action'),
            'message': message if message else _('The action has been queued'),
        })

        return self

    def _notify_update(self, records):
        users = []

        for record in records:
            if record.user_id and record.user_id not in users:
                users.append(record.user_id)

        if users:
            for user in users:
                self.env['bus.bus']._sendone(user.partner_id, 'queue_job_updated', {})

    def _notify_update_state(self, records, values):
        run_changed = ('date_enqueued' in values
                       or 'date_started' in values
                       or 'date_stopped' in values
                       or 'date_cancelled' in values
                       or 'date_done' in values
                       or 'date_failed' in values)
        notify_records = []

        if run_changed:
            for record in records:
                unlinked = False

                if (record.auto_unlink == DELAY_AUTO_UNLINK_DONE
                        and not record.log_count and record.state in ['done', 'cancelled']):
                    unlinked = True
                elif record.auto_unlink == DELAY_AUTO_UNLINK_FULL:
                    unlinked = True

                if not unlinked:
                    notify_records.append(record)

        if notify_records:
            self._notify_update(notify_records)
