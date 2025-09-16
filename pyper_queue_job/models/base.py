# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from datetime import datetime

from odoo import models

from .pyper_queue_job import DELAY_AUTO_UNLINK_FULL

from ..utils import serialize


class Base(models.AbstractModel):
    _inherit = 'base'

    def with_delay(
        self,
        name: str = None,
        user_id: models.Model | int = None,
        company_id: models.Model | int = None,
        auto_unlink: str = None,
        date_enqueued: datetime = None,
        **payload
    ):
        """
        Allow to execute function asynchronously and use it simply like this:::
            self.with_delay(auto_unlink='none').action_done()
        ``with_delay()`` accepts job properties which specify how the job will
        be executed.
        The ids of the recordset are automatically restored in the model instance instancied by the job process.
        By default, the current user and current company are restored in the model instance instancied by the job
        process.
        :param name: The custom job name
        :param user_id: The user used for the job
        :param company_id: The active company used for the job
        :param auto_unlink: Defined if the job is deleted after done only (Done) or done/fail/cancel (Fail) or none
        :param date_enqueued: Date when the job is planned
        :param payload: The payload for the job
        :return: Delayable: The wrapper to delay the called method just after the method with_delay() to run in the
                            future with a queue job
        """
        return Delayable(self, **{
            'name': name,
            'user_id': user_id,
            'company_id': company_id,
            'auto_unlink': auto_unlink,
            'date_enqueued': date_enqueued,
            **payload,
        })


class Delayable(object):
    def __init__(self, recordset, **job_config):
        self.recordset = recordset
        self.job_config = job_config
        self.method_name = None

    def __getattr__(self, name, *args, **kwargs):
        if self.method_name is None:
            self.method_name = name

        return self._call_method

    def _call_method(self, *args, **kwargs):
        if self.method_name is None:
            pass

        payload = {**kwargs}

        if args:
            payload.update({'_args': args})

        job_vals = {
            **self.job_config,
            'model_name': self.recordset._name,
            'model_method': self.method_name,
            'recordset_ids': self.recordset.ids if self.recordset.ids else False,
            'payload': serialize(payload),
        }

        if job_vals.get('name', None) is None:
            job_vals['name'] = self.recordset._name + ':' + self.method_name + '()'

        user_id = job_vals.get('user_id', None)
        if isinstance(user_id, models.Model):
            job_vals['user_id'] = job_vals.get('user_id').id
        elif user_id is None:
            job_vals['user_id'] = self.recordset.env.user.id

        company_id = job_vals.get('company_id', None)
        if isinstance(company_id, models.Model):
            job_vals['company_id'] = job_vals.get('company_id').id
        elif user_id is None:
            job_vals['company_id'] = self.recordset.env.company.id

        if job_vals.get('date_enqueued', None) is None:
            job_vals['date_enqueued'] = datetime.now()

        if job_vals.get('auto_unlink', None) is None:
            job_vals['auto_unlink'] = DELAY_AUTO_UNLINK_FULL

        return self.recordset.env['pyper.queue.job'].sudo().create(job_vals)
