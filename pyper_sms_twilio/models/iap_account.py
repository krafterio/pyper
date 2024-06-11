# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models


class IapAccount(models.Model):
    _inherit = 'iap.account'

    provider = fields.Selection(
        selection_add=[
            ('sms_twilio', 'SMS Twilio'),
        ],
        ondelete={'sms_twilio': 'cascade'},
    )

    twilio_account_sid = fields.Char(
        string='Twilio Account SID',
    )

    twilio_auth_token = fields.Char(
        string='Twilio Auth Token',
    )

    twilio_phone_number = fields.Char(
        string='Twilio Phone Number',
        help='The phone number use to send SMS messages'
    )

    def _get_service_from_provider(self):
        if self.provider == 'sms_twilio':
            return 'sms'
