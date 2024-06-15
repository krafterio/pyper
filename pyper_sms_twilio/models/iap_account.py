# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from odoo import fields, models
from odoo.tools.config import config


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
        return 'sms' if self.provider == 'sms_twilio' else super()._get_service_from_provider()

    def _check_provider_balance_enable(self):
        return True if self.provider == 'sms_twilio' else super()._check_provider_balance_enable()

    def _get_provider_unit_name(self):
        return 'SMS' if self.provider == 'sms_twilio' else super()._get_provider_unit_name()

    def _get_force_allowed_add_balance_users(self):
        return (super()._get_force_allowed_add_balance_users()
                + config.get('sms_twilio_update_balance_allowed_users', '').split(','))
