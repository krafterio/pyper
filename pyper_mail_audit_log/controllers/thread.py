# Copyright Krafter SAS <hey@krafter.io>
# LGPL-3 License (see LICENSE file).

from odoo import http
from odoo.http import request
from odoo.addons.mail.controllers.thread import ThreadController as BaseThreadController


class ThreadController(BaseThreadController):
    @http.route('/mail/thread/messages', methods=['POST'], type='jsonrpc', auth='user')
    def mail_thread_messages(self, thread_model, thread_id, fetch_params=None, audit_log=False):
        request.update_context(mail_message_without_audit_log=not audit_log)

        return super().mail_thread_messages(thread_model, thread_id, fetch_params)
