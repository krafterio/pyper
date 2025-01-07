# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

import pytz

from datetime import datetime

from odoo import fields, models


class MailMessage(models.Model):
    _inherit = 'mail.message'

    message_type = fields.Selection(
        selection_add=[
            ('phone_outbound', 'Phone outbound'),
            ('phone_inbound', 'Phone inbound'),
        ],
        ondelete={
            'phone_outbound': 'set comment',
            'phone_inbound': 'set comment',
        }
    )

    phone_event = fields.Selection(
        selection=[
            ('ringing', 'Ringing'),
            ('answered', 'Answered'),
            ('hangup', 'Hangup'),
            ('missed', 'Missed'),
        ],
        string='Phone event',
    )

    phone_call_duration = fields.Float(
        'Phone call duration',
        help='Duration in seconds',
    )

    phone_from_number = fields.Char(
        'Phone from number',
    )

    phone_to_number = fields.Char(
        'Phone to number',
    )

    def ringover_phone_call_log(self, payload: dict):
        event = payload.get('event')
        data = payload.get('data')

        if not event or not data or not isinstance(data, dict):
            return self.env.user

        direction = data.get('direction')
        call_id = data.get('call_id')
        message_id = '<' + call_id + '@ringover>' if call_id else False
        start_time = data.get('start_time')
        from_number = self._phone_format(number=data.get('from_number'))
        to_number = self._phone_format(number=data.get('to_number'))
        tmz = pytz.timezone(self.env.user.tz or 'UTC')

        if direction not in ('outbound', 'inbound') or self.env['mail.message'].search([('message_id', '=', message_id)], limit=1):
            return self.env.user

        def search_partner(number):
            return self.env['res.partner'].search([
                '|',
                ('phone_formatted', '=', number),
                ('mobile_formatted', '=', number),
            ], limit=1)

        def create_partner(number):
            return self.env['res.partner'].create({
                'name': from_number,
                'phone': from_number,
            })

        if direction == 'outbound':
            author_partner = search_partner(from_number) or self.env.ref('base.user_root').partner_id
            res_partner = search_partner(to_number) or create_partner(to_number)
        else:
            # Associate caller like model partner and receiver like author
            author_partner = search_partner(to_number) or create_partner(to_number)
            res_partner = search_partner(from_number) or self.env.ref('base.user_root').partner_id

        vals = {
            'message_type': 'phone_' + direction,
            'subtype_id': self.env.ref('mail.mt_activities').id,
            'mail_activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
            'message_id': '<' + call_id + '@ringover>' if call_id else False,
            'date': datetime.fromtimestamp(start_time, pytz.UTC).astimezone(tmz).replace(tzinfo=None) if start_time else False,
            'phone_event': event if any(opt[0] == event for opt in self._fields['phone_event'].selection) else False,
            'phone_call_duration': data.get('duration_in_seconds', 0),
            'phone_from_number': from_number,
            'phone_to_number': to_number,
            'author_id': author_partner.id,
            'model': 'res.partner',
            'res_id': res_partner.id,
            'is_internal': True,
        }

        return self.env['mail.message'].create(vals)

    def _message_format_extras(self, format_reply):
        self.ensure_one()
        vals = super()._message_format_extras(format_reply)
        vals.update({
            'message_type_name': next((l for v, l in self._fields['message_type'].selection if v == self.message_type), False),
            'phone_event': self.phone_event,
            'phone_event_name': next((l for v, l in self._fields['phone_event'].selection if v == self.phone_event), False),
            'phone_call_duration': self.phone_call_duration,
            'phone_from_number': self._phone_format(number=self.phone_from_number, force_format='INTERNATIONAL') if self.phone_from_number else False,
            'phone_to_number': self._phone_format(number=self.phone_to_number, force_format='INTERNATIONAL') if self.phone_to_number else False,
        })

        return vals
