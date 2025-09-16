# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

import logging
import re

from math import ceil

from odoo import _, models, tools
from odoo.exceptions import UserError

from ..tools.sms_twilio_api import SmsTwilioApi

_logger = logging.getLogger(__name__)


class SmsSms(models.Model):
    _inherit = 'sms.sms'

    def _split_batch(self):
        if self.env['iap.account'].get('sms').provider == 'sms_twilio':
            # No batch with Twilio SMS
            for record in self:
                yield [record.id]
        else:
            yield from super()._split_batch()

    def _send(self, unlink_failed=False, unlink_sent=True, raise_exception=False):
        iap_account = self.env['iap.account'].get('sms')
        count_sms_enabled = iap_account.provider_balance_enable and iap_account.provider_balance_enabled

        if iap_account.provider != 'sms_twilio':
            super()._send(unlink_failed, unlink_sent, raise_exception)

        # Send with Twilio SMS
        messages = [{
            'count': count_sms(body) if count_sms_enabled else 0,
            'content': body,
            'numbers': [{'number': sms.number, 'uuid': sms.uuid} for sms in body_sms_records],
        } for body, body_sms_records in self.grouped('body').items()]

        # Count SMS to send
        count_sms_to_send = 0.0
        if count_sms_enabled:
            for message in messages:
                count_sms_to_send += message['count']

        try:
            if iap_account.provider_balance - count_sms_to_send < 0:
                raise UserError(_('The balance is insufficient to send SMS'))

            results = SmsTwilioApi(self.env).send_sms_batch(messages)
        except Exception as e:
            _logger.info('Sent batch %s Twilio SMS: %s: failed with exception %s', len(self.ids), self.ids, e)
            if raise_exception:
                raise
            results = [{'uuid': sms.uuid, 'state': 'server_error'} for sms in self]
        else:
            _logger.info('Send batch %s Twilio SMS: %s: gave %s', len(self.ids), self.ids, results)

        results_uuids = [result['uuid'] for result in results]
        all_sms_sudo = self.env['sms.sms'].sudo().search([('uuid', 'in', results_uuids)]).with_context(
            sms_skip_msg_notification=True)

        for iap_state, results_group in tools.groupby(results, key=lambda result: result['state']):
            sms_sudo = all_sms_sudo.filtered(lambda s: s.uuid in {result['uuid'] for result in results_group})

            if success_state := self.IAP_TO_SMS_STATE_SUCCESS.get(iap_state):
                sms_sudo.sms_tracker_id._action_update_from_sms_state(success_state)
                to_delete = {'to_delete': True} if unlink_sent else {}
                sms_sudo.write({'state': success_state, 'failure_type': False, **to_delete})
                for result_group in results_group:
                    iap_account.provider_balance -= result_group.get('count', 0)
            else:
                failure_type = self.IAP_TO_SMS_FAILURE_TYPE.get(iap_state, 'unknown')

                if failure_type != 'unknown':
                    sms_sudo.sms_tracker_id._action_update_from_sms_state('error', failure_type=failure_type, failure_reason=results_group[0].get('message', False))
                else:
                    sms_sudo.sms_tracker_id._action_update_from_provider_error(iap_state)

                to_delete = {'to_delete': True} if unlink_failed else {}
                sms_sudo.write({'state': 'error', 'failure_type': failure_type, **to_delete})

        all_sms_sudo.mail_message_id._notify_message_notification_update()


def count_sms(content):
    size = len(content)
    encoding = extract_encoding(content)

    if size == 0:
        return 0

    if encoding == 'UNICODE':
        if size <= 70:
            return 1

        return ceil(size / 67)

    if size <= 160:
        return 1

    return ceil(size / 153)


def extract_encoding(content):
    res = re.match("^[@£$¥èéùìòÇ\\nØø\\rÅåΔ_ΦΓΛΩΠΨΣΘΞÆæßÉ !\\\"#¤%&'()*+,-./0123456789:;<=>?¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿abcdefghijklmnopqrstuvwxyzäöñüà]*$", content)

    return 'GSM7' if res else 'UNICODE'
