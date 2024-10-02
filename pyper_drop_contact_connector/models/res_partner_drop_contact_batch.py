# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import json

import requests

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.addons.pyper_queue_job.exceptions import QueueJobProcessError


class ResPartnerDropContactBatch(models.Model):
    _name = 'res.partner.drop_contact.batch'
    _inherit = ['pyper.queue.job.batch.mixin']
    _description = 'Drop contact batch information for Partners'
    _order = 'create_date DESC'

    state = fields.Selection(
        selection_add=[
            ('getting_request', 'Getting Request'),
            ('waiting_info', 'Waiting info'),
            ('getting_info', 'Getting Info'),
            ('waiting',),
        ],
    )

    partner_ids = fields.One2many(
        'res.partner',
        'drop_contact_batch_id',
        'Partners',
        required=True,
    )

    partner_count = fields.Integer(
        'Partner count',
        compute='_compute_partner_count',
    )

    request_id = fields.Char(
        'Request ID',
    )

    response_data = fields.Text(
        'Response data',
    )

    @api.depends('partner_ids')
    def _compute_partner_count(self):
        for item in self:
            item.partner_count = len(item.partner_ids.ids)

    def _reset_values(self):
        super()._reset_values()
        self.state = 'waiting_info' if self.request_id else 'enqueued'
        self.response_data = False

        return True

    def retrieve_info(self):
        try:
            self.ensure_one()

            if self.partner_count > 250 or self.partner_count == 0:
                raise QueueJobProcessError(_('The action to enrich contact info can accept only 250 contacts by batch'))

            if self.state == 'enqueued':
                self._getting_request_id()

            elif self.state == 'waiting_info':
                self._getting_info()

        except Exception as err:
            self._raise_exception(err)

    def _getting_request_id(self):
        if self.state not in ['getting_request']:
            self.state = 'getting_request'
            self.env.cr.commit()

        params = self.env['ir.config_parameter'].sudo()
        endpoint_api = params.get_param('drop_contact_connector.endpoint_api', '')
        token_api = params.get_param('drop_contact_connector.token_api', '')
        data = {
            'data': [],
            'language': 'fr',
        }

        for partner in self.partner_ids:
            data['data'].append({
                'full_name': partner.name,
                'company': partner.parent_id.name,
                'email': partner.email,
            })

        res = requests.post(
            endpoint_api + '/batch',
            json=data,
            headers={
                'Content-Type': 'application/json',
                'X-Access-Token': token_api,
            },
        )

        ResPartnerDropContactBatch._validate_response(res)
        res_data = res.json()

        if res_data['success'] is True and res_data['request_id']:
            self.request_id = res_data['request_id']
            self.state = 'waiting_info'
            self.env.cr.commit()

            # Schedule the next step
            self.with_delay(date_enqueued=datetime.now() + relativedelta(seconds=30)).retrieve_info()
        else:
            raise QueueJobProcessError(_('Service returned an invalid request id'))

    def _getting_info(self):
        if self.state not in ['waiting_info']:
            self.state = 'getting_info'
            self.env.cr.commit()

        if self.response_data:
            res_data = json.loads(self.response_data)
        else:
            params = self.env['ir.config_parameter'].sudo()
            endpoint_api = params.get_param('drop_contact_connector.endpoint_api', '')
            token_api = params.get_param('drop_contact_connector.token_api', '')
            res = requests.get(
                endpoint_api + '/batch/{}'.format(self.request_id),
                headers={
                    'Content-Type': 'application/json',
                    'X-Access-Token': token_api,
                },
            )

            ResPartnerDropContactBatch._validate_response(res)
            res_data = res.json()

            # Response is not ready, retry in 30s
            if not res_data['success'] and not res_data['error']:
                self.state = 'waiting_info'
                self.env.cr.commit()

                # Schedule the next step
                self.with_delay(date_enqueued=datetime.now() + relativedelta(seconds=30)).retrieve_info()
                return

            self.response_data = json.dumps(res_data, indent=4)
            self.env.cr.commit()

        data = res_data['data']
        if self.partner_count != len(data):
            raise QueueJobProcessError(_('The number of partners to enrich and the number of contacts returned by the service are different'))

        for idx, partner in enumerate(self.partner_ids):
            self.enrich_partner(partner, data[idx])

        self.state = 'done'
        self.env.cr.commit()

    def enrich_partner(self, partner_id, info):
        if 'email' in info and not partner_id.email:
            partner_id.email = info['email'][0]['email']

        if 'website' in info and not partner_id.website:
            partner_id.website = info['website']

        if 'full_name' in info and not partner_id.name:
            partner_id.name = info['full_name']

        if 'phone' in info and not partner_id.phone:
            partner_id.phone = info['phone']

        if 'linkedin' in info and not partner_id.linkedin_url:
            partner_id.linkedin_url = info['linkedin']

        self.env.cr.commit()

    @staticmethod
    def _validate_response(res):
        if not res.ok:
            if res.status_code == 400:
                raise QueueJobProcessError(_('Invalid request'))
            if res.status_code == 401:
                raise QueueJobProcessError(_('Invalid API Token'))
            if res.status_code == 403:
                raise QueueJobProcessError(_('Exceeded quota'))
            if res.status_code == 404:
                raise QueueJobProcessError(_('Resource not found'))
            if res.status_code == 429:
                raise QueueJobProcessError(_('Too many requests in a given slot of time'))
            if res.status_code == 500:
                raise QueueJobProcessError(_('Drop Contact have been informed of this and will solve it'))
            if res.status_code == 503:
                raise QueueJobProcessError(_('Drop Contact temporarily offline for maintenance'))
            if res.status_code == 503:
                raise QueueJobProcessError(_('Gateway timeout'))
            if res.status_code == 524:
                raise QueueJobProcessError(_('A timeout occured'))
