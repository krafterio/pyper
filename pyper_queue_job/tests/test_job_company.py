# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

"""tests: the company carried by a job, and the company it runs with."""

from unittest.mock import patch

from odoo.tests.common import TransactionCase

from ..models import base


class TestJobCompany(TransactionCase):

    def setUp(self):
        super().setUp()
        self.record = self.env['res.partner'].create({'name': 'Job target'})

    def _enqueue(self, **job_config):
        """Create a real job: ``Delayable`` skips creation in test mode."""
        with patch.object(base, 'config', {'test_enable': False}):
            self.record.with_delay(**job_config).read()

        return self.env['pyper.queue.job'].search(
            [('model_name', '=', 'res.partner')], order='id desc', limit=1,
        )

    # -- Company stored on the job -----------------------------------------

    def test_company_defaults_to_the_environment_company(self):
        job = self._enqueue(name='job without company')
        self.assertEqual(job.company_id, self.env.company)

    def test_explicit_user_does_not_drop_the_company_default(self):
        # Regression: the fallback used to test ``user_id``, so passing a
        # user (as any connector dispatch does) left the job companyless,
        # and a companyless job empties ``env.company`` at execution.
        job = self._enqueue(
            name='job with user', user_id=self.env.ref('base.user_admin'),
        )
        self.assertEqual(job.company_id, self.env.company)

    def test_explicit_company_is_kept(self):
        other = self.env['res.company'].create({'name': 'Other company'})
        job = self._enqueue(name='job with company', company_id=other)
        self.assertEqual(job.company_id, other)

    # -- Company the job runs with -----------------------------------------

    def test_context_pins_the_job_company(self):
        job = self._enqueue(name='job to run')
        self.assertEqual(
            job._job_company_context(),
            {'allowed_company_ids': job.company_id.ids},
        )

    def test_context_is_empty_when_the_job_has_no_company(self):
        # Companyless jobs exist in the wild (enqueued from a public
        # webhook before the fix above): they must fall back to the
        # runner company instead of running with ``env.company`` empty.
        job = self._enqueue(name='job to run')
        job.sudo().company_id = False
        self.assertEqual(job._job_company_context(), {})

    def test_context_of_an_empty_recordset_is_empty(self):
        self.assertEqual(
            self.env['pyper.queue.job']._job_company_context(), {},
        )
