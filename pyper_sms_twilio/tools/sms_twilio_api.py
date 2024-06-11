# Copyright Krafter SAS <hey@krafter.io>
# Krafter Proprietary License (see LICENSE file).

from requests import post
from requests.auth import HTTPBasicAuth

from requests_toolbelt import MultipartEncoder


class SmsTwilioApi:
    DEFAULT_ENDPOINT = 'https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Messages.json'

    def __init__(self, env):
        self.env = env

    def _contact_twilio_sms(self, params, timeout=15):
        account = self.env['iap.account'].get('sms')
        url = self.DEFAULT_ENDPOINT.format(AccountSid=account.twilio_account_sid)
        auth = HTTPBasicAuth(account.twilio_account_sid, account.twilio_auth_token)
        results = []

        for message in params.get('messages'):
            for number in message.get('numbers'):
                payload = MultipartEncoder(
                    fields={
                        'From': account.twilio_phone_number,
                        'To': number.get('number'),
                        'Body': message.get('content'),
                    }
                )

                try:
                    if account.provider != 'sms_twilio':
                        raise Exception('Twilio provider is required to send SMS')

                    response = post(
                        url,
                        headers={
                            'Content-Type': payload.content_type,
                        },
                        data=payload,
                        auth=auth,
                        timeout=timeout,
                    )

                    if response.status_code == 201:
                        results.append({
                            'uuid': number.get('uuid'),
                            'state': 'success',
                            'credit': '0 Credits',
                        })
                    else:
                        data = response.json()
                        results.append({
                            'uuid': number.get('uuid'),
                            'state': 'server_error',
                            'credit': '0 Credits',
                            'message': data.get('message'),
                        })
                except Exception as e:
                    results.append({
                        'uuid': number.get('uuid'),
                        'state': 'server_error',
                        'credit': '0 Credits',
                        'message': str(e),
                    })

        return results

    def send_sms_batch(self, messages):
        """ Send SMS using Twilio in batch mode.

        :param list messages: list of SMS (grouped by content) to send:
          formatted as ```[
              {
                  'content' : str,
                  'numbers' : [
                      { 'uuid' : str, 'number' : str },
                      { 'uuid' : str, 'number' : str },
                      ...
                  ]
              }, ...
          ]```
        :return: response from the endpoint called, which is a list of results
          formatted as ```[
              {
                  uuid: UUID of the request,
                  state: ONE of: {
                      'success', 'processing', 'server_error', 'unregistered', 'insufficient_credit',
                      'wrong_number_format', 'duplicate_message', 'country_not_supported', 'registration_needed',
                  },
                  credit: Optional: Credits spent to send SMS (provided if the actual price is known)
              }, ...
          ]```
        """
        return self._contact_twilio_sms({
            'messages': messages,
            'webhook_url': None,
            'dbuuid': self.env['ir.config_parameter'].sudo().get_param('database.uuid')
        })
